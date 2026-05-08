from abc import ABC, abstractmethod
from api.domain.metrics import ProductivityMetrics

class FeedbackRule(ABC):
    @abstractmethod
    def match(self, metrics: ProductivityMetrics) -> bool:
        pass

    @abstractmethod
    def get_message(self) -> str:
        pass

class ExhaustiveHyperfocusRule(FeedbackRule):
    def match(self, metrics: ProductivityMetrics) -> bool:
        return metrics.indice_esgotamento >= 2.0 and metrics.media_foco >= 4.0

    def get_message(self) -> str:
        return (
            "Hiperfoco Exaustivo: Foco excelente, mas com alto custo energético. "
            "Recomendamos uma pausa para descanso cognitivo antes de iniciar o próximo bloco de tarefas."
        )

class MagicalSymbiosisRule(FeedbackRule):
    def match(self, metrics: ProductivityMetrics) -> bool:
        return metrics.taxa_uso_ia >= 50.0 and metrics.media_energia >= 3.0

    def get_message(self) -> str:
        return (
            "Simbiose com IA: O apoio da inteligência artificial otimizou suas entregas "
            "e ajudou a poupar sua energia mental."
        )

class MentalFogRule(FeedbackRule):
    def match(self, metrics: ProductivityMetrics) -> bool:
        return metrics.media_foco < 2.5

    def get_message(self) -> str:
        return (
            "Neblina Mental: Nível de foco abaixo do esperado. Experimente mudar de ambiente, "
            "beber água ou dividir sua próxima meta em tarefas menores."
        )

class SustainableFlowRule(FeedbackRule):
    def match(self, metrics: ProductivityMetrics) -> bool:
        return 3.0 <= metrics.media_foco <= 4.5 and metrics.media_energia >= 3.5

    def get_message(self) -> str:
        return (
            "Fluxo Sustentável: Excelente equilíbrio entre foco e energia! "
            "Você manteve um ritmo constante e produtivo sem se esgotar."
        )

class DefaultFeedbackRule(FeedbackRule):
    def match(self, metrics: ProductivityMetrics) -> bool:
        return True

    def get_message(self) -> str:
        return (
            "Sessão registrada. Continue acompanhando suas métricas para "
            "identificar seus padrões ideais de foco e produtividade."
        )

class FeedbackEvaluator:
    def __init__(self):
        # A ordem das regras define a prioridade de avaliação
        self._rules = [
            ExhaustiveHyperfocusRule(),
            MagicalSymbiosisRule(),
            MentalFogRule(),
            SustainableFlowRule(),
            DefaultFeedbackRule(),
        ]

    def evaluate(self, metrics: ProductivityMetrics) -> str:
        for rule in self._rules:
            if rule.match(metrics):
                return rule.get_message()
        # Fallback de segurança (embora DefaultFeedbackRule sempre retorne True)
        return "Sessão registrada."
