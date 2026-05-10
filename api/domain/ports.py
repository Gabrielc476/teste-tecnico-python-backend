from abc import ABC, abstractmethod
from api.domain.entities import FocusLog
from api.domain.metrics import ProductivityMetrics

class FocusLogRepository(ABC):
    @abstractmethod
    async def save(self, log: FocusLog) -> FocusLog:
        """
        Persiste de forma assíncrona um registro de foco e retorna o objeto salvo.
        """
        pass

    @abstractmethod
    async def get_aggregated_metrics(self) -> ProductivityMetrics:
        """
        Calcula e retorna as métricas consolidadas diretamente via banco de dados de forma assíncrona.
        """
        pass

