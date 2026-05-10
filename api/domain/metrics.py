from dataclasses import dataclass
from typing import ClassVar

@dataclass(frozen=True)
class ProductivityMetrics:
    # Constantes de limiar (Thresholds) para avaliação de saúde cognitiva
    LIMIT_EXHAUSTION_INDEX: ClassVar[float] = 2.0
    LIMIT_HIGH_FOCUS: ClassVar[float] = 4.0
    LIMIT_SYMBIOSIS_IA_RATE: ClassVar[float] = 50.0
    LIMIT_SYMBIOSIS_ENERGY: ClassVar[float] = 3.0
    LIMIT_FOG_FOCUS: ClassVar[float] = 2.5
    LIMIT_FLOW_MIN_FOCUS: ClassVar[float] = 3.0
    LIMIT_FLOW_MAX_FOCUS: ClassVar[float] = 4.5
    LIMIT_FLOW_ENERGY: ClassVar[float] = 3.5

    media_foco: float
    media_energia: float
    tempo_total_focado: int
    taxa_uso_ia: float
    indice_esgotamento: float
    total_sessoes: int

    def is_exhaustive_hyperfocus(self) -> bool:
        """Foco excelente com alto esgotamento cognitivo."""
        return self.indice_esgotamento >= self.LIMIT_EXHAUSTION_INDEX and self.media_foco >= self.LIMIT_HIGH_FOCUS

    def is_magical_symbiosis(self) -> bool:
        """Identifica uso produtivo de IA com preservação de energia."""
        return self.taxa_uso_ia >= self.LIMIT_SYMBIOSIS_IA_RATE and self.media_energia >= self.LIMIT_SYMBIOSIS_ENERGY

    def is_mental_fog(self) -> bool:
        """Alerta de neblina mental se o foco for persistentemente baixo."""
        return self.media_foco < self.LIMIT_FOG_FOCUS

    def is_sustainable_flow(self) -> bool:
        """Estado ideal equilibrado de energia e atenção."""
        return self.LIMIT_FLOW_MIN_FOCUS <= self.media_foco <= self.LIMIT_FLOW_MAX_FOCUS and self.media_energia >= self.LIMIT_FLOW_ENERGY

    def evaluate_feedback(self) -> str:
        """
        Avalia as métricas consolidadas e retorna a mensagem de feedback apropriada.
        Segue uma ordem estrita de prioridades de avaliação de saúde cognitiva.
        """
        if self.total_sessoes == 0:
            return "Nenhuma sessão registrada ainda. Comece a registrar sessões para visualizar seus padrões!"

        if self.is_exhaustive_hyperfocus():
            return (
                "Hiperfoco Exaustivo: Foco excelente, mas com alto custo energético. "
                "Recomendamos uma pausa para descanso cognitivo antes de iniciar o próximo bloco de tarefas."
            )

        if self.is_magical_symbiosis():
            return (
                "Simbiose com IA: O apoio da inteligência artificial otimizou suas entregas "
                "e ajudou a poupar sua energia mental."
            )

        if self.is_mental_fog():
            return (
                "Neblina Mental: Nível de foco abaixo do esperado. Experimente mudar de ambiente, "
                "beber água ou dividir sua próxima meta em tarefas menores."
            )

        if self.is_sustainable_flow():
            return (
                "Fluxo Sustentável: Excelente equilíbrio entre foco e energia! "
                "Você manteve um ritmo constante e produtivo sem se esgotar."
            )

        return (
            "Sessão registrada. Continue acompanhando suas métricas para "
            "identificar seus padrões ideais de foco e produtividade."
        )

