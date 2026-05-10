import pystray
from PIL import Image, ImageDraw
import threading
import json
import os
import time
from datetime import datetime
import customtkinter as ctk
import requests

SESSION_FILE = ".current_session.json"
OFFLINE_QUEUE = "offline_queue.json"
API_URL = "http://127.0.0.1:8000"

def create_image(active=False):
    # Generates a solid colored icon
    color = "green" if active else "gray"
    image = Image.new('RGB', (64, 64), color=(255, 255, 255))
    dc = ImageDraw.Draw(image)
    dc.ellipse((16, 16, 48, 48), fill=color)
    return image

class FocusTracker:
    def __init__(self):
        self.icon = None
        self.is_tracking = False
        self.start_time = None
        self.check_active_session()
        
    def check_active_session(self):
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, 'r') as f:
                    data = json.load(f)
                    start_str = data.get("start_time")
                    if start_str:
                        self.start_time = datetime.fromisoformat(start_str)
                        self.is_tracking = True
            except Exception:
                os.remove(SESSION_FILE)
                
    def save_session(self):
        if self.start_time:
            with open(SESSION_FILE, 'w') as f:
                json.dump({"start_time": self.start_time.isoformat()}, f)
                
    def toggle_tracking(self, icon, item):
        if self.is_tracking:
            self.stop_tracking()
        else:
            self.start_tracking()

    def start_tracking(self):
        self.start_time = datetime.now()
        self.is_tracking = True
        self.save_session()
        self.update_icon()

    def stop_tracking(self):
        if not self.is_tracking:
            return
            
        end_time = datetime.now()
        duration = end_time - self.start_time
        minutos = int(duration.total_seconds() // 60)
        
        # Mínimo de 1 minuto para não perder sessões super curtas acidentais (ou teste)
        if minutos < 1:
            minutos = 1
            
        self.is_tracking = False
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
            
        self.update_icon()
        
        # Inicia a UI do popup no thread principal via uma chamada separada
        # Não podemos bloquear a thread do pystray
        threading.Thread(target=self.show_popup, args=(minutos,), daemon=True).start()

    def sync_offline(self, icon=None, item=None):
        if not os.path.exists(OFFLINE_QUEUE):
            return
            
        try:
            with open(OFFLINE_QUEUE, 'r') as f:
                queue = json.load(f)
        except Exception:
            queue = []
            
        if not queue:
            return
            
        remaining = []
        for payload in queue:
            try:
                resp = requests.post(f"{API_URL}/registro-foco", json=payload, timeout=5)
                if resp.status_code not in (200, 201):
                    remaining.append(payload)
            except requests.RequestException:
                remaining.append(payload)
                
        with open(OFFLINE_QUEUE, 'w') as f:
            json.dump(remaining, f)

    def show_popup(self, minutos):
        # Configure CustomTkinter
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        app = ctk.CTk()
        app.title("Sessão Concluída")
        app.geometry("400x520")
        app.attributes("-topmost", True)
        
        # Centralizar na tela
        app.eval('tk::PlaceWindow . center')
        
        # Title
        title = ctk.CTkLabel(app, text=f"Foco Encerrado: {minutos} minutos", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=(20, 10))
        
        # Foco
        foco_lbl = ctk.CTkLabel(app, text="Nível de Foco (1-5):")
        foco_lbl.pack(pady=(10, 0))
        foco_slider = ctk.CTkSlider(app, from_=1, to=5, number_of_steps=4)
        foco_slider.set(3)
        foco_slider.pack(pady=5)
        
        # Energia
        energia_lbl = ctk.CTkLabel(app, text="Nível de Energia (1-5):")
        energia_lbl.pack(pady=(10, 0))
        energia_slider = ctk.CTkSlider(app, from_=1, to=5, number_of_steps=4)
        energia_slider.set(3)
        energia_slider.pack(pady=5)
        
        # IA Auxiliou
        ia_var = ctk.BooleanVar(value=False)
        ia_check = ctk.CTkCheckBox(app, text="A Inteligência Artificial auxiliou na tarefa?", variable=ia_var)
        ia_check.pack(pady=15)
        
        # Comentario
        coment_lbl = ctk.CTkLabel(app, text="O que foi feito? (Opcional se foco for médio)")
        coment_lbl.pack(pady=(10, 0))
        coment_entry = ctk.CTkEntry(app, width=300)
        coment_entry.pack(pady=5)
        
        error_lbl = ctk.CTkLabel(app, text="", text_color="red")
        error_lbl.pack()
        
        def save():
            comentario = coment_entry.get().strip()
            foco = int(foco_slider.get())
            energia = int(energia_slider.get())
            ia = ia_var.get()
            
            # Fricção reduzida: comentário só é obrigatório nos extremos (1 ou 5)
            if not comentario and (foco == 1 or foco == 5):
                error_lbl.configure(text="Comentário é obrigatório para focos extremos.")
                return
                
            payload = {
                "nivel_foco": foco,
                "nivel_energia": energia,
                "tempo_minutos": minutos,
                "comentario": comentario or "Sessão regular",
                "ia_auxiliou": ia
            }
            
            # Enviar para a API
            try:
                resp = requests.post(f"{API_URL}/registro-foco", json=payload, timeout=5)
                resp.raise_for_status()
            except requests.RequestException:
                # API Offline: Usar Fila (Outbox)
                queue = []
                if os.path.exists(OFFLINE_QUEUE):
                    try:
                        with open(OFFLINE_QUEUE, 'r') as f:
                            queue = json.load(f)
                    except Exception:
                        pass
                queue.append(payload)
                with open(OFFLINE_QUEUE, 'w') as f:
                    json.dump(queue, f)
            
            app.destroy()
            
        def cancel():
            # Apenas fecha a janela sem registrar
            app.destroy()
            
        btn_save = ctk.CTkButton(app, text="Salvar Sessão", command=save, fg_color="green", hover_color="darkgreen")
        btn_save.pack(pady=10)
        
        btn_cancel = ctk.CTkButton(app, text="Descartar", command=cancel, fg_color="transparent", text_color="gray", hover_color="#333333")
        btn_cancel.pack(pady=0)
        
        app.mainloop()

    def update_icon(self):
        if self.icon:
            self.icon.icon = create_image(self.is_tracking)
            menu = (
                pystray.MenuItem("Parar Foco" if self.is_tracking else "Iniciar Foco", self.toggle_tracking, default=True),
                pystray.MenuItem("Sincronizar Offline", self.sync_offline),
                pystray.MenuItem("Sair", self.quit)
            )
            self.icon.menu = menu

    def quit(self, icon, item):
        icon.stop()

    def run(self):
        menu = (
            pystray.MenuItem("Parar Foco" if self.is_tracking else "Iniciar Foco", self.toggle_tracking, default=True),
            pystray.MenuItem("Sincronizar Offline", self.sync_offline),
            pystray.MenuItem("Sair", self.quit)
        )
        self.icon = pystray.Icon("foco_tdah", create_image(self.is_tracking), "Foco TDAH", menu)
        
        # Sincroniza logo ao ligar (se houver API e conexão)
        threading.Thread(target=self.sync_offline, daemon=True).start()
        
        self.icon.run()

if __name__ == "__main__":
    tracker = FocusTracker()
    tracker.run()
