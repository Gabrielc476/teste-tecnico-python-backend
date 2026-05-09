from fastapi import Depends
from sqlmodel import Session
from api.infrastructure.database import get_session
from api.infrastructure.repository import SQLiteFocusLogRepository
from api.usecases.register_focus_session import RegisterFocusSessionUseCase
from api.usecases.generate_diagnostics import GenerateProductivityDiagnosticsUseCase

def get_register_use_case(
    session: Session = Depends(get_session)
) -> RegisterFocusSessionUseCase:
    """Instancia o caso de uso de registro de sessão injetando o repositório concreto."""
    repository = SQLiteFocusLogRepository(session)
    return RegisterFocusSessionUseCase(repository)

def get_diagnostics_use_case(
    session: Session = Depends(get_session)
) -> GenerateProductivityDiagnosticsUseCase:
    """Instancia o caso de uso de geração de diagnósticos injetando o repositório concreto."""
    repository = SQLiteFocusLogRepository(session)
    return GenerateProductivityDiagnosticsUseCase(repository)
