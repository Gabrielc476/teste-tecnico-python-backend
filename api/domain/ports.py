from abc import ABC, abstractmethod
from typing import List
from api.domain.entities import FocusLog

class FocusLogRepository(ABC):
    @abstractmethod
    def save(self, log: FocusLog) -> FocusLog:
        """
        Persiste um registro de foco e retorna o objeto salvo.
        """
        pass

    @abstractmethod
    def find_all(self) -> List[FocusLog]:
        """
        Retorna todos os registros de foco persistidos.
        """
        pass
