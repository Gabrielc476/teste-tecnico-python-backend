from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from api.infrastructure.database import engine
from api.infrastructure.routes import router

# Cria as tabelas do banco de dados na inicialização (se não existirem)
SQLModel.metadata.create_all(engine)

app = FastAPI(
    title="Foco TDAH API",
    description="API de Log de Performance e Foco com métricas de esgotamento e simbiose com IA.",
    version="1.0.0",
)

# Permitir comunicação local do Client Desktop com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra as rotas de negócio
app.include_router(router)

@app.get("/health", tags=["Health"])
def health_check():
    """
    Endpoint simples para verificar se o servidor está online.
    """
    return {"status": "ok", "message": "Foco TDAH API rodando perfeitamente."}

