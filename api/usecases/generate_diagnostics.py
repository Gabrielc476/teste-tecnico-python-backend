from dataclasses import dataclass
from api.domain.ports import FocusLogRepository
from api.domain.metrics import MetricsCalculator
from api.domain.strategies import FeedbackEvaluator

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
        self._calculator = MetricsCalculator
        self._evaluator = FeedbackEvaluator()

    def execute(self) -> DiagnosticsResult:
        """
        Gera o diagnóstico completo consolidando todos os registros de foco do repositório.
        Retorna DiagnosticsResult com valores zerados se não houver registros.
        """
        logs = self._repository.find_all()
        if not logs:
            return DiagnosticsResult(
                media_foco=0.0,
                media_energia=0.0,
                tempo_total_focado=0,
                indice_esgotamento=0.0,
                taxa_uso_ia=0.0,
                mensagem_feedback="Nenhuma sessão registrada ainda. Comece a registrar sessões para visualizar seus padrões!",
                total_sessoes=0
            )

        metrics = self._calculator.gerar_diagnostico(logs)
        feedback = self._evaluator.evaluate(metrics)

        return DiagnosticsResult(
            media_foco=round(metrics.media_foco, 2),
            media_energia=round(metrics.media_energia, 2),
            tempo_total_focado=metrics.tempo_total_focado,
            indice_esgotamento=round(metrics.indice_esgotamento, 2),
            taxa_uso_ia=round(metrics.taxa_uso_ia, 1),
            mensagem_feedback=feedback,
            total_sessoes=len(logs)
        )
