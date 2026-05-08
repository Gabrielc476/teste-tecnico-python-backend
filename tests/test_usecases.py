import unittest
from datetime import datetime
from typing import List

from api.domain.entities import FocusLog
from api.domain.ports import FocusLogRepository
from api.usecases.register_focus_session import RegisterFocusSessionUseCase
from api.usecases.generate_diagnostics import GenerateProductivityDiagnosticsUseCase, DiagnosticsResult

class InMemoryFocusLogRepository(FocusLogRepository):
    def __init__(self):
        self._logs: List[FocusLog] = []

    def save(self, log: FocusLog) -> FocusLog:
        self._logs.append(log)
        return log

    def find_all(self) -> List[FocusLog]:
        return self._logs

class TestUseCases(unittest.TestCase):
    def setUp(self):
        self.repository = InMemoryFocusLogRepository()
        self.register_usecase = RegisterFocusSessionUseCase(self.repository)
        self.diagnostics_usecase = GenerateProductivityDiagnosticsUseCase(self.repository)

    def test_register_session_success(self):
        log = self.register_usecase.execute(
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
        self.assertEqual(len(self.repository.find_all()), 1)

    def test_register_session_invalid_values(self):
        with self.assertRaises(ValueError):
            self.register_usecase.execute(
                nivel_foco=6, # Inválido
                nivel_energia=3,
                tempo_minutos=30,
                comentario="Invalido",
                ia_auxiliou=False
            )

    def test_register_session_empty_comment(self):
        with self.assertRaises(ValueError):
            self.register_usecase.execute(
                nivel_foco=4,
                nivel_energia=4,
                tempo_minutos=20,
                comentario="   ", # Comentário vazio/com espaços
                ia_auxiliou=False
            )

    def test_register_session_with_category(self):
        log = self.register_usecase.execute(
            nivel_foco=4,
            nivel_energia=4,
            tempo_minutos=25,
            comentario="Escrevendo documentacao",
            ia_auxiliou=False,
            categoria="coding"
        )
        self.assertEqual(log.categoria, "coding")

    def test_diagnostics_no_logs(self):
        result = self.diagnostics_usecase.execute()
        self.assertIsInstance(result, DiagnosticsResult)
        self.assertEqual(result.total_sessoes, 0)
        self.assertEqual(result.media_foco, 0.0)
        self.assertEqual(result.media_energia, 0.0)
        self.assertEqual(result.tempo_total_focado, 0)
        self.assertEqual(result.indice_esgotamento, 0.0)
        self.assertEqual(result.taxa_uso_ia, 0.0)
        self.assertIn("Nenhuma sessão registrada", result.mensagem_feedback)

    def test_diagnostics_exhaustive_hyperfocus(self):
        # indice_esgotamento >= 2.0 e media_foco >= 4.0
        # Foco = 5, Energia = 1 -> Diferença = 4
        self.register_usecase.execute(
            nivel_foco=5, nivel_energia=1, tempo_minutos=40,
            comentario="Hiperfocado focado sem energia", ia_auxiliou=False
        )
        
        result = self.diagnostics_usecase.execute()
        self.assertEqual(result.total_sessoes, 1)
        self.assertEqual(result.media_foco, 5.0)
        self.assertEqual(result.media_energia, 1.0)
        self.assertEqual(result.tempo_total_focado, 40)
        self.assertEqual(result.indice_esgotamento, 4.0)
        self.assertEqual(result.taxa_uso_ia, 0.0)
        self.assertIn("Hiperfoco Exaustivo", result.mensagem_feedback)

    def test_diagnostics_magical_symbiosis(self):
        # taxa_uso_ia >= 50% e media_energia >= 3.0
        self.register_usecase.execute(nivel_foco=4, nivel_energia=4, tempo_minutos=30, comentario="Sessao 1", ia_auxiliou=True)
        self.register_usecase.execute(nivel_foco=4, nivel_energia=4, tempo_minutos=30, comentario="Sessao 2", ia_auxiliou=True)
        self.register_usecase.execute(nivel_foco=4, nivel_energia=4, tempo_minutos=30, comentario="Sessao 3", ia_auxiliou=False)

        result = self.diagnostics_usecase.execute()
        self.assertEqual(result.total_sessoes, 3)
        self.assertEqual(result.taxa_uso_ia, 66.7)
        self.assertEqual(result.media_energia, 4.0)
        self.assertIn("Simbiose com IA", result.mensagem_feedback)

if __name__ == "__main__":
    import time
    
    start_time = time.perf_counter()
    
    # Executa a suite de testes manualmente para podermos medir o tempo exato
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUseCases)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    end_time = time.perf_counter()
    
    duration_ms = (end_time - start_time) * 1000
    duration_us = (end_time - start_time) * 1000000
    
    print("\n" + "="*60)
    print(" MEDICÃO DE ALTA PRECISÃO (time.perf_counter)")
    print(f" Tempo total decorrido: {duration_ms:.4f} milissegundos (ms)")
    print(f" Tempo total decorrido: {duration_us:.1f} microsegundos (us)")
    print(f" Tempo médio por teste: {duration_us / 7:.1f} microsegundos (us)")
    print("="*60 + "\n")

