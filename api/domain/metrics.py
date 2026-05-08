from dataclasses import dataclass
from typing import List
from api.domain.entities import FocusLog

@dataclass(frozen=True)
class ProductivityMetrics:
    media_foco: float
    media_energia: float
    tempo_total_focado: int
    taxa_uso_ia: float
    indice_esgotamento: float

class MetricsCalculator:
    @staticmethod
    def calcular_media_foco(logs: List[FocusLog]) -> float:
        if not logs:
            return 0.0
        return sum(log.nivel_foco for log in logs) / len(logs)

    @staticmethod
    def calcular_media_energia(logs: List[FocusLog]) -> float:
        if not logs:
            return 0.0
        return sum(log.nivel_energia for log in logs) / len(logs)

    @staticmethod
    def calcular_tempo_total(logs: List[FocusLog]) -> int:
        return sum(log.tempo_minutos for log in logs)

    @staticmethod
    def calcular_taxa_uso_ia(logs: List[FocusLog]) -> float:
        if not logs:
            return 0.0
        sessoes_com_ia = sum(1 for log in logs if log.ia_auxiliou)
        return (sessoes_com_ia / len(logs)) * 100.0

    @staticmethod
    def calcular_indice_esgotamento(logs: List[FocusLog]) -> float:
        if not logs:
            return 0.0
        soma_diferencas = sum(max(0, log.nivel_foco - log.nivel_energia) for log in logs)
        return soma_diferencas / len(logs)

    @classmethod
    def gerar_diagnostico(cls, logs: List[FocusLog]) -> ProductivityMetrics:
        return ProductivityMetrics(
            media_foco=cls.calcular_media_foco(logs),
            media_energia=cls.calcular_media_energia(logs),
            tempo_total_focado=cls.calcular_tempo_total(logs),
            taxa_uso_ia=cls.calcular_taxa_uso_ia(logs),
            indice_esgotamento=cls.calcular_indice_esgotamento(logs)
        )
