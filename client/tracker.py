import pystray
from PIL import Image, ImageDraw
import threading
import json
import os
import time
from datetime import datetime
import customtkinter as ctk
import requests
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

SESSION_FILE = ".current_session.json"
OFFLINE_QUEUE = "offline_queue.json"
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# Lock para sincronização de acesso concorrente aos arquivos de sessão e fila offline
FILE_LOCK = threading.Lock()

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
        with FILE_LOCK:
            if os.path.exists(SESSION_FILE):
                try:
                    with open(SESSION_FILE, 'r') as f:
                        data = json.load(f)
                        start_str = data.get("start_time")
                        if start_str:
                            self.start_time = datetime.fromisoformat(start_str)
                            self.is_tracking = True
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"[WARNING] Session file corrupted, recreating: {e}")
                    try:
                        os.remove(SESSION_FILE)
                    except OSError:
                        pass
                except OSError as e:
                    print(f"[ERROR] OS error reading session file: {e}")
                
    def save_session(self):
        if self.start_time:
            with FILE_LOCK:
                try:
                    with open(SESSION_FILE, 'w') as f:
                        json.dump({"start_time": self.start_time.isoformat()}, f)
                except OSError as e:
                    print(f"[ERROR] Failed to save session file: {e}")
                
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
        with FILE_LOCK:
            if os.path.exists(SESSION_FILE):
                try:
                    os.remove(SESSION_FILE)
                except OSError as e:
                    print(f"[ERROR] Failed to remove session file: {e}")
            
        self.update_icon()
        
        # Inicia a UI do popup no thread principal via uma chamada separada
        # Não podemos bloquear a thread do pystray
        threading.Thread(target=self.show_popup, args=(minutos,), daemon=True).start()

    def sync_offline(self, icon=None, item=None):
        with FILE_LOCK:
            if not os.path.exists(OFFLINE_QUEUE):
                return
                
            try:
                with open(OFFLINE_QUEUE, 'r') as f:
                    queue = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                print(f"[ERROR] Failed to read offline queue: {e}")
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
                
        with FILE_LOCK:
            try:
                with open(OFFLINE_QUEUE, 'w') as f:
                    json.dump(remaining, f)
            except OSError as e:
                print(f"[ERROR] Failed to write offline queue: {e}")

    def show_popup(self, minutos):
        # Configure CustomTkinter
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        app = ctk.CTk()
        app.title("Sessão Concluída")
        app.geometry("400x600")
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
        
        # Categoria
        categoria_lbl = ctk.CTkLabel(app, text="Categoria:")
        categoria_lbl.pack(pady=(10, 0))
        categoria_options = ["Trabalho", "Estudo", "Projeto Pessoal", "Reunião", "Leitura", "Outros"]
        categoria_var = ctk.StringVar(value="Trabalho")
        categoria_menu = ctk.CTkOptionMenu(app, values=categoria_options, variable=categoria_var)
        categoria_menu.pack(pady=5)

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
            categoria = categoria_var.get()
            
            # Fricção reduzida: comentário só é obrigatório nos extremos (1 ou 5)
            if not comentario and (foco == 1 or foco == 5):
                error_lbl.configure(text="Comentário é obrigatório para focos extremos.")
                return
                
            payload = {
                "nivel_foco": foco,
                "nivel_energia": energia,
                "tempo_minutos": minutos,
                "comentario": comentario or "Sessão regular",
                "ia_auxiliou": ia,
                "categoria": categoria
            }
            
            # Enviar para a API
            try:
                resp = requests.post(f"{API_URL}/registro-foco", json=payload, timeout=5)
                resp.raise_for_status()
            except requests.RequestException:
                # API Offline: Usar Fila (Outbox)
                with FILE_LOCK:
                    queue = []
                    if os.path.exists(OFFLINE_QUEUE):
                        try:
                            with open(OFFLINE_QUEUE, 'r') as f:
                                queue = json.load(f)
                        except (json.JSONDecodeError, OSError) as e:
                            print(f"[WARNING] Offline queue corrupted or unreadable, recreating: {e}")
                    queue.append(payload)
                    try:
                        with open(OFFLINE_QUEUE, 'w') as f:
                            json.dump(queue, f)
                    except OSError as e:
                        print(f"[ERROR] Failed to save session to offline queue: {e}")
            
            app.destroy()
            
        def cancel():
            # Apenas fecha a janela sem registrar
            app.destroy()
            
        btn_save = ctk.CTkButton(app, text="Salvar Sessão", command=save, fg_color="green", hover_color="darkgreen")
        btn_save.pack(pady=10)
        
        btn_cancel = ctk.CTkButton(app, text="Descartar", command=cancel, fg_color="transparent", text_color="gray", hover_color="#333333")
        btn_cancel.pack(pady=0)
        
        app.mainloop()

    def open_diagnostics(self, icon, item):
        threading.Thread(target=self.show_diagnostics_popup, daemon=True).start()

    def show_diagnostics_popup(self):
        try:
            resp = requests.get(f"{API_URL}/diagnostico-produtividade", timeout=5)
            resp.raise_for_status()
            data = resp.json()
        except Exception:
            data = {"mensagem_feedback": "Não foi possível conectar à API localmente.", "total_sessoes": 0}

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        app = ctk.CTk()
        app.title("Diagnóstico de Produtividade")
        app.geometry("450x420")
        app.attributes("-topmost", True)
        app.eval('tk::PlaceWindow . center')
        
        title = ctk.CTkLabel(app, text="Seu Diagnóstico", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=(20, 10))
        
        metrics_frame = ctk.CTkFrame(app)
        metrics_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(metrics_frame, text=f"Total de Sessões: {data.get('total_sessoes', 0)}").pack(pady=2)
        ctk.CTkLabel(metrics_frame, text=f"Tempo Total: {data.get('tempo_total_focado', 0)} minutos").pack(pady=2)
        ctk.CTkLabel(metrics_frame, text=f"Foco Médio: {data.get('media_foco', 0)}/5").pack(pady=2)
        ctk.CTkLabel(metrics_frame, text=f"Energia Média: {data.get('media_energia', 0)}/5").pack(pady=2)
        ctk.CTkLabel(metrics_frame, text=f"Índice de Esgotamento: {data.get('indice_esgotamento', 0)}").pack(pady=2)
        ctk.CTkLabel(metrics_frame, text=f"Uso de IA: {data.get('taxa_uso_ia', 0)}%").pack(pady=2)
        
        feedback_lbl = ctk.CTkLabel(app, text=data.get('mensagem_feedback', ''), wraplength=400, justify="center")
        feedback_lbl.pack(pady=15, padx=10)
        
        btn_close = ctk.CTkButton(app, text="Fechar", command=app.destroy)
        btn_close.pack(pady=10)
        
        app.mainloop()

    def update_icon(self):
        if self.icon:
            self.icon.icon = create_image(self.is_tracking)
            menu = (
                pystray.MenuItem("Parar Foco" if self.is_tracking else "Iniciar Foco", self.toggle_tracking, default=True),
                pystray.MenuItem("Ver Diagnóstico", self.open_diagnostics),
                pystray.MenuItem("Sincronizar Offline", self.sync_offline),
                pystray.MenuItem("Sair", self.quit)
            )
            self.icon.menu = menu

    def quit(self, icon, item):
        icon.stop()

    def run(self):
        menu = (
            pystray.MenuItem("Parar Foco" if self.is_tracking else "Iniciar Foco", self.toggle_tracking, default=True),
            pystray.MenuItem("Ver Diagnóstico", self.open_diagnostics),
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
