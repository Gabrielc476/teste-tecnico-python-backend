from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from api.domain.entities import FocusLog

class FocusLogModel(SQLModel, table=True):
    __tablename__ = "focus_logs"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    nivel_foco: int = Field(..., ge=1, le=5)
    nivel_energia: int = Field(..., ge=1, le=5)
    tempo_minutos: int = Field(..., gt=0)
    comentario: str
    ia_auxiliou: bool
    categoria: Optional[str] = None
    data_registro: datetime = Field(default_factory=datetime.now)

    @classmethod
    def from_domain(cls, log: FocusLog) -> "FocusLogModel":
        """Converte uma entidade de domínio pura em um modelo ORM SQLModel."""
        return cls(
            id=str(log.id),
            nivel_foco=log.nivel_foco,
            nivel_energia=log.nivel_energia,
            tempo_minutos=log.tempo_minutos,
            comentario=log.comentario,
            ia_auxiliou=log.ia_auxiliou,
            categoria=log.categoria,
            data_registro=log.data_registro
        )

    def to_domain(self) -> FocusLog:
        """Converte este modelo ORM SQLModel de volta para a entidade de domínio pura."""
        return FocusLog(
            id=UUID(self.id),
            nivel_foco=self.nivel_foco,
            nivel_energia=self.nivel_energia,
            tempo_minutos=self.tempo_minutos,
            comentario=self.comentario,
            ia_auxiliou=self.ia_auxiliou,
            categoria=self.categoria,
            data_registro=self.data_registro
        )
