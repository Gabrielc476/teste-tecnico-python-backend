from dataclasses import dataclass
from api.domain.ports import FocusLogRepository

@dataclass(frozen=True)
class DiagnosticsResult:
    media_foco: float
    media_energia: float
    tempo_total_focado: int
    indice_esgotamento: float
    taxa_uso_ia: float
    mensagem_feedback: str
    total_sessoes: int

class GenerateProductivityDiagnosticsUseCase:
    def __init__(self, repository: FocusLogRepository):
        self._repository = repository

    async def execute(self) -> DiagnosticsResult:
        """
        Gera de forma assíncrona o diagnóstico completo consolidando os registros de foco do repositório.
        Retorna DiagnosticsResult com valores zerados se não houver registros.
        """
        metrics = await self._repository.get_aggregated_metrics()
        feedback = metrics.evaluate_feedback()

        return DiagnosticsResult(
            media_foco=round(metrics.media_foco, 2),
            media_energia=round(metrics.media_energia, 2),
            tempo_total_focado=metrics.tempo_total_focado,
            indice_esgotamento=round(metrics.indice_esgotamento, 2),
            taxa_uso_ia=round(metrics.taxa_uso_ia, 1),
            mensagem_feedback=feedback,
            total_sessoes=metrics.total_sessoes
        )

