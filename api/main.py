from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.infrastructure.database import init_db
from api.infrastructure.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cria as tabelas de forma assíncrona se não existirem
    await init_db()
    yield

app = FastAPI(
    title="Foco TDAH API",
    description="API de Log de Performance e Foco com métricas de esgotamento e simbiose com IA.",
    version="1.0.0",
    lifespan=lifespan,
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

