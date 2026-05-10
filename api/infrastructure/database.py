import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./api/infrastructure/focus.db")

# Garante que a pasta pai do banco sqlite exista se for um arquivo local
if DATABASE_URL.startswith("sqlite:///"):
    db_path = DATABASE_URL.replace("sqlite:///", "")
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    # Converte para usar o driver assíncrono aiosqlite
    DATABASE_URL = DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")

# Cria o engine com configurações específicas para SQLite (check_same_thread)
engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

async def init_db():
    """Inicializa as tabelas de forma assíncrona."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    """Generator que fornece uma sessão de banco ativa e assíncrona para cada request."""
    async with AsyncSession(engine) as session:
        yield session
