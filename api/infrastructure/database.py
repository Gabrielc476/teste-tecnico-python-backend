import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./api/infrastructure/focus.db")

# Garante que a pasta pai do banco sqlite exista se for um arquivo local
if DATABASE_URL.startswith("sqlite:///"):
    db_path = DATABASE_URL.replace("sqlite:///", "")
    # Tratando caminhos relativos
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)

# Cria o engine com configurações específicas para SQLite (check_same_thread)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

def get_session():
    """Generator que fornece uma sessão de banco ativa para cada request."""
    with Session(engine) as session:
        yield session
