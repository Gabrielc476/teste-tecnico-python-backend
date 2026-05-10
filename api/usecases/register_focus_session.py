from typing import Optional
from api.domain.entities import FocusLog
from api.domain.ports import FocusLogRepository

class RegisterFocusSessionUseCase:
    def __init__(self, repository: FocusLogRepository):
        self._repository = repository

    async def execute(self, nivel_foco: int, nivel_energia: int, tempo_minutos: int,
                comentario: str, ia_auxiliou: bool, categoria: Optional[str] = None) -> FocusLog:
        """
        Executa de forma assíncrona a lógica de negócio para criação e persistência de uma nova sessão de foco.
        Levanta ValueError se nivel_foco, nivel_energia, tempo_minutos ou comentario forem inválidos.
        """
        # A instanciação da entidade FocusLog valida as invariantes de negócio via __post_init__
        log = FocusLog(
            nivel_foco=nivel_foco,
            nivel_energia=nivel_energia,
            tempo_minutos=tempo_minutos,
            comentario=comentario,
            ia_auxiliou=ia_auxiliou,
            categoria=categoria
        )
        return await self._repository.save(log)


