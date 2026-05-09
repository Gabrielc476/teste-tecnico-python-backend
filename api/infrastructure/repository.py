from typing import List
from sqlmodel import Session, select
from api.domain.entities import FocusLog
from api.domain.ports import FocusLogRepository
from api.infrastructure.models import FocusLogModel

class SQLiteFocusLogRepository(FocusLogRepository):
    def __init__(self, session: Session):
        self._session = session

    def save(self, log: FocusLog) -> FocusLog:
        """Persiste um FocusLog no banco SQLModel e retorna a entidade mapeada."""
        model = FocusLogModel.from_domain(log)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return model.to_domain()

    def find_all(self) -> List[FocusLog]:
        """Busca todos os FocusLogs no banco e retorna como instâncias de domínio."""
        statement = select(FocusLogModel)
        models = self._session.exec(statement).all()
        return [m.to_domain() for m in models]
