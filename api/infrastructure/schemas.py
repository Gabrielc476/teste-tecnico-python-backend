from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FocusLogRequest(BaseModel):
    """Schema de entrada para POST /registro-foco."""
    nivel_foco: int = Field(..., ge=1, le=5, description="Nível de foco (1-5)")
    nivel_energia: Optional[int] = Field(None, ge=1, le=5, description="Nível de energia (1-5)")
    tempo_minutos: int = Field(..., gt=0, description="Duração da sessão em minutos")
    comentario: str = Field(..., min_length=1, description="O que foi feito ou o que causou distração")
    ia_auxiliou: Optional[bool] = Field(None, description="Se a inteligência artificial auxiliou na sessão")
    categoria: Optional[str] = Field(None, description="Categoria opcional da atividade (ex: coding, reunião)")

class FocusLogResponse(BaseModel):
    """Schema de resposta para POST /registro-foco."""
    id: str
    nivel_foco: int
    nivel_energia: int
    tempo_minutos: int
    comentario: str
    ia_auxiliou: bool
    categoria: Optional[str]
    data_registro: datetime
