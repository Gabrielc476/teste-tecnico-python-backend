import unittest
from datetime import datetime
from typing import List

from api.domain.entities import FocusLog
from api.domain.ports import FocusLogRepository
from api.domain.metrics import ProductivityMetrics
from api.usecases.register_focus_session import RegisterFocusSessionUseCase
from api.usecases.generate_diagnostics import GenerateProductivityDiagnosticsUseCase, DiagnosticsResult

class InMemoryFocusLogRepository(FocusLogRepository):
    def __init__(self):
        self._logs: List[FocusLog] = []

    async def save(self, log: FocusLog) -> FocusLog:
        self._logs.append(log)
        return log

    async def get_aggregated_metrics(self) -> ProductivityMetrics:
        if not self._logs:
            return ProductivityMetrics(
                media_foco=0.0,
                media_energia=0.0,
                tempo_total_focado=0,
                taxa_uso_ia=0.0,
                indice_esgotamento=0.0,
                total_sessoes=0
            )

        total_sessoes = len(self._logs)
        media_foco = sum(log.nivel_foco for log in self._logs) / total_sessoes
        media_energia = sum(log.nivel_energia for log in self._logs) / total_sessoes
        tempo_total_focado = sum(log.tempo_minutos for log in self._logs)
        
        sessoes_com_ia = sum(1 for log in self._logs if log.ia_auxiliou)
        taxa_uso_ia = (sessoes_com_ia / total_sessoes) * 100.0

        soma_esgotamento = sum(max(0, log.nivel_foco - log.nivel_energia) for log in self._logs)
        indice_esgotamento = soma_esgotamento / total_sessoes

        return ProductivityMetrics(
            media_foco=media_foco,
            media_energia=media_energia,
            tempo_total_focado=tempo_total_focado,
            taxa_uso_ia=taxa_uso_ia,
            indice_esgotamento=indice_esgotamento,
            total_sessoes=total_sessoes
        )

class TestUseCases(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.repository = InMemoryFocusLogRepository()
        self.register_usecase = RegisterFocusSessionUseCase(self.repository)
        self.diagnostics_usecase = GenerateProductivityDiagnosticsUseCase(self.repository)

    async def test_register_session_success(self):
        log = await self.register_usecase.execute(
            nivel_foco=4,
            nivel_energia=5,
            tempo_minutos=30,
            comentario="Implementando casos de uso",
            ia_auxiliou=True
        )
        self.assertIsInstance(log, FocusLog)
        self.assertEqual(log.nivel_foco, 4)
        self.assertEqual(log.nivel_energia, 5)
        self.assertEqual(log.tempo_minutos, 30)
        self.assertEqual(log.comentario, "Implementando casos de uso")
        self.assertTrue(log.ia_auxiliou)
        
        metrics = await self.repository.get_aggregated_metrics()
        self.assertEqual(metrics.total_sessoes, 1)

    async def test_register_session_invalid_values(self):
        with self.assertRaises(ValueError):
            await self.register_usecase.execute(
                nivel_foco=6, # Inválido
                nivel_energia=3,
                tempo_minutos=30,
                comentario="Invalido",
                ia_auxiliou=False
            )

    async def test_register_session_empty_comment(self):
        with self.assertRaises(ValueError):
            await self.register_usecase.execute(
                nivel_foco=4,
                nivel_energia=4,
                tempo_minutos=20,
                comentario="   ", # Comentário vazio/com espaços
                ia_auxiliou=False
            )

    async def test_register_session_with_category(self):
        log = await self.register_usecase.execute(
            nivel_foco=4,
            nivel_energia=4,
            tempo_minutos=25,
            comentario="Escrevendo documentacao",
            ia_auxiliou=False,
            categoria="coding"
        )
        self.assertEqual(log.categoria, "coding")

    async def test_diagnostics_no_logs(self):
        result = await self.diagnostics_usecase.execute()
        self.assertIsInstance(result, DiagnosticsResult)
        self.assertEqual(result.total_sessoes, 0)
        self.assertEqual(result.media_foco, 0.0)
        self.assertEqual(result.media_energia, 0.0)
        self.assertEqual(result.tempo_total_focado, 0)
        self.assertEqual(result.indice_esgotamento, 0.0)
        self.assertEqual(result.taxa_uso_ia, 0.0)
        self.assertIn("Nenhuma sessão registrada", result.mensagem_feedback)

    async def test_diagnostics_exhaustive_hyperfocus(self):
        await self.register_usecase.execute(
            nivel_foco=5, nivel_energia=1, tempo_minutos=40,
            comentario="Hiperfocado focado sem energia", ia_auxiliou=False
        )
        
        result = await self.diagnostics_usecase.execute()
        self.assertEqual(result.total_sessoes, 1)
        self.assertEqual(result.media_foco, 5.0)
        self.assertEqual(result.media_energia, 1.0)
        self.assertEqual(result.tempo_total_focado, 40)
        self.assertEqual(result.indice_esgotamento, 4.0)
        self.assertEqual(result.taxa_uso_ia, 0.0)
        self.assertIn("Hiperfoco Exaustivo", result.mensagem_feedback)

    async def test_diagnostics_magical_symbiosis(self):
        await self.register_usecase.execute(nivel_foco=4, nivel_energia=4, tempo_minutos=30, comentario="Sessao 1", ia_auxiliou=True)
        await self.register_usecase.execute(nivel_foco=4, nivel_energia=4, tempo_minutos=30, comentario="Sessao 2", ia_auxiliou=True)
        await self.register_usecase.execute(nivel_foco=4, nivel_energia=4, tempo_minutos=30, comentario="Sessao 3", ia_auxiliou=False)

        result = await self.diagnostics_usecase.execute()
        self.assertEqual(result.total_sessoes, 3)
        self.assertEqual(result.taxa_uso_ia, 66.7)
        self.assertEqual(result.media_energia, 4.0)
        self.assertIn("Simbiose com IA", result.mensagem_feedback)

if __name__ == "__main__":
    import time
    
    start_time = time.perf_counter()
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUseCases)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    end_time = time.perf_counter()
    duration_ms = (end_time - start_time) * 1000
    
    print("\n" + "="*60)
    print(" MEDICÃO DE ALTA PRECISÃO (time.perf_counter)")
    print(f" Tempo total decorrido: {duration_ms:.4f} milissegundos (ms)")
    print("="*60 + "\n")


