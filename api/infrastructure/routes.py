from fastapi import APIRouter, Depends, HTTPException
from api.infrastructure.schemas import FocusLogRequest, FocusLogResponse
from api.infrastructure.container import get_register_use_case, get_diagnostics_use_case
from api.usecases.register_focus_session import RegisterFocusSessionUseCase
from api.usecases.generate_diagnostics import GenerateProductivityDiagnosticsUseCase, DiagnosticsResult

router = APIRouter()

@router.post("/registro-foco", response_model=FocusLogResponse, status_code=201, tags=["Sessões de Foco"])
def registrar_foco(
    payload: FocusLogRequest,
    use_case: RegisterFocusSessionUseCase = Depends(get_register_use_case),
):
    """
    Registra um novo bloco de trabalho encerrado.
    Valida as regras de entrada e armazena de forma persistente.
    """
    try:
        log = use_case.execute(
            nivel_foco=payload.nivel_foco,
            nivel_energia=payload.nivel_energia,
            tempo_minutos=payload.tempo_minutos,
            comentario=payload.comentario,
            ia_auxiliou=payload.ia_auxiliou,
            categoria=payload.categoria,
        )
        return FocusLogResponse(
            id=str(log.id),
            nivel_foco=log.nivel_foco,
            nivel_energia=log.nivel_energia,
            tempo_minutos=log.tempo_minutos,
            comentario=log.comentario,
            ia_auxiliou=log.ia_auxiliou,
            categoria=log.categoria,
            data_registro=log.data_registro,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/diagnostico-produtividade", response_model=DiagnosticsResult, tags=["Diagnóstico"])
def diagnostico_produtividade(
    use_case: GenerateProductivityDiagnosticsUseCase = Depends(get_diagnostics_use_case),
):
    """
    Retorna o diagnóstico inteligente de produtividade compilando todas as sessões registradas.
    """
    return use_case.execute()
