from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

@dataclass
class FocusLog:
    nivel_foco: int
    nivel_energia: int
    tempo_minutos: int
    ia_auxiliou: bool
    data_registro: datetime = field(default_factory=datetime.now)
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        # Validação simples de domínio (embora o caso de uso e pydantic também validem)
        if not (1 <= self.nivel_foco <= 5):
            raise ValueError("nivel_foco deve estar entre 1 e 5")
        if not (1 <= self.nivel_energia <= 5):
            raise ValueError("nivel_energia deve estar entre 1 e 5")
        if self.tempo_minutos < 0:
            raise ValueError("tempo_minutos deve ser positivo")
