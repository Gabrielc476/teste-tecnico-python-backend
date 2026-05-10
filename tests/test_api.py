import unittest
import asyncio
from fastapi.testclient import TestClient
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from api.main import app
from api.infrastructure.database import get_session

# Banco de dados de teste assíncrono em memória
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)

async def override_get_session():
    async with AsyncSession(test_engine) as session:
        yield session

class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Sobrescreve a dependência de sessão do FastAPI para usar o banco de dados de teste
        app.dependency_overrides[get_session] = override_get_session
        
    @classmethod
    def tearDownClass(cls):
        app.dependency_overrides.clear()

    def setUp(self):
        # Inicializa as tabelas do banco de dados em memória de forma síncrona
        # usando um loop de eventos temporário
        async def init_tables():
            async with test_engine.begin() as conn:
                await conn.run_sync(SQLModel.metadata.create_all)
        asyncio.run(init_tables())

    def tearDown(self):
        # Destrói as tabelas para garantir total isolamento entre os testes
        async def drop_tables():
            async with test_engine.begin() as conn:
                await conn.run_sync(SQLModel.metadata.drop_all)
        asyncio.run(drop_tables())

    def test_registrar_foco_success(self):
        with TestClient(app) as client:
            payload = {
                "nivel_foco": 4,
                "nivel_energia": 4,
                "tempo_minutos": 30,
                "comentario": "Sessão de teste de integração assíncrona",
                "ia_auxiliou": True,
                "categoria": "coding"
            }
            response = client.post("/registro-foco", json=payload)
            self.assertEqual(response.status_code, 201)
            data = response.json()
            self.assertEqual(data["nivel_foco"], 4)
            self.assertEqual(data["nivel_energia"], 4)
            self.assertEqual(data["tempo_minutos"], 30)
            self.assertEqual(data["comentario"], "Sessão de teste de integração assíncrona")
            self.assertTrue(data["ia_auxiliou"])
            self.assertEqual(data["categoria"], "coding")
            self.assertIn("id", data)

    def test_registrar_foco_invalid_payload(self):
        with TestClient(app) as client:
            payload = {
                "nivel_foco": 6, # Limite superior é 5
                "nivel_energia": 4,
                "tempo_minutos": 30,
                "comentario": "Sessão de foco inválida",
                "ia_auxiliou": False
            }
            response = client.post("/registro-foco", json=payload)
            self.assertEqual(response.status_code, 422)

    def test_diagnostico_produtividade_flow(self):
        with TestClient(app) as client:
            # 1. Obter diagnóstico com banco vazio
            response = client.get("/diagnostico-produtividade")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["total_sessoes"], 0)
            self.assertEqual(data["media_foco"], 0.0)
            self.assertEqual(data["media_energia"], 0.0)
            self.assertEqual(data["tempo_total_focado"], 0)
            self.assertEqual(data["indice_esgotamento"], 0.0)
            self.assertEqual(data["taxa_uso_ia"], 0.0)
            self.assertIn("Nenhuma sessão registrada", data["mensagem_feedback"])

            # 2. Registrar sessão que gera "Hiperfoco Exaustivo" (Foco=5, Energia=1)
            client.post("/registro-foco", json={
                "nivel_foco": 5,
                "nivel_energia": 1,
                "tempo_minutos": 45,
                "comentario": "Trabalhando até o limite",
                "ia_auxiliou": False
            })

            # 3. Validar se o diagnóstico retornou corretamente as métricas e o feedback correto
            response = client.get("/diagnostico-produtividade")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["total_sessoes"], 1)
            self.assertEqual(data["media_foco"], 5.0)
            self.assertEqual(data["media_energia"], 1.0)
            self.assertEqual(data["tempo_total_focado"], 45)
            self.assertEqual(data["indice_esgotamento"], 4.0)
            self.assertEqual(data["taxa_uso_ia"], 0.0)
            self.assertIn("Hiperfoco Exaustivo", data["mensagem_feedback"])

            # 4. Registrar mais sessões para induzir "Simbiose com IA" (IA >= 50%, Energia >= 3)
            client.post("/registro-foco", json={
                "nivel_foco": 4, "nivel_energia": 4, "tempo_minutos": 30,
                "comentario": "Trabalho auxiliado por Copilot", "ia_auxiliou": True
            })
            client.post("/registro-foco", json={
                "nivel_foco": 4, "nivel_energia": 4, "tempo_minutos": 30,
                "comentario": "Trabalho auxiliado por ChatGPT", "ia_auxiliou": True
            })

            # 5. Validar o diagnóstico agregado
            response = client.get("/diagnostico-produtividade")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["total_sessoes"], 3)
            # Focos: (5 + 4 + 4) / 3 = 13/3 = 4.33
            # Energias: (1 + 4 + 4) / 3 = 9/3 = 3.0
            # Esgotamentos: s1 = 4, s2 = 0, s3 = 0 -> Médio = 4/3 = 1.33
            # Uso de IA: 2 / 3 = 66.7%
            self.assertEqual(data["media_foco"], 4.33)
            self.assertEqual(data["media_energia"], 3.0)
            self.assertEqual(data["tempo_total_focado"], 105)
            self.assertEqual(data["indice_esgotamento"], 1.33)
            self.assertEqual(data["taxa_uso_ia"], 66.7)
            self.assertIn("Simbiose com IA", data["mensagem_feedback"])

if __name__ == "__main__":
    unittest.main()
