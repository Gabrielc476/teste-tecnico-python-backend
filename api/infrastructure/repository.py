from sqlalchemy import select, func, case
from sqlmodel.ext.asyncio.session import AsyncSession
from api.domain.entities import FocusLog
from api.domain.ports import FocusLogRepository
from api.domain.metrics import ProductivityMetrics
from api.infrastructure.models import FocusLogModel

class SQLiteFocusLogRepository(FocusLogRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, log: FocusLog) -> FocusLog:
        """Persiste de forma assíncrona um FocusLog no banco SQLModel e retorna a entidade mapeada."""
        model = FocusLogModel.from_domain(log)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return model.to_domain()

    async def get_aggregated_metrics(self) -> ProductivityMetrics:
        """Calcula as métricas diretamente no SQLite usando agregação nativa (CQRS)."""
        statement = select(
            func.count(FocusLogModel.id).label("total_sessoes"),
            func.avg(FocusLogModel.nivel_foco).label("media_foco"),
            func.avg(FocusLogModel.nivel_energia).label("media_energia"),
            func.sum(FocusLogModel.tempo_minutos).label("tempo_total_focado"),
            func.sum(case((FocusLogModel.ia_auxiliou == True, 1), else_=0)).label("sessoes_com_ia"),
            func.sum(case((FocusLogModel.nivel_foco > FocusLogModel.nivel_energia, FocusLogModel.nivel_foco - FocusLogModel.nivel_energia), else_=0)).label("soma_esgotamento")
        )
        result = await self._session.exec(statement)
        row = result.first()


        if not row or row.total_sessoes == 0:
            return ProductivityMetrics(
                media_foco=0.0,
                media_energia=0.0,
                tempo_total_focado=0,
                taxa_uso_ia=0.0,
                indice_esgotamento=0.0,
                total_sessoes=0
            )

        total_sessoes = row.total_sessoes
        sessoes_com_ia = row.sessoes_com_ia or 0
        soma_esgotamento = row.soma_esgotamento or 0

        return ProductivityMetrics(
            media_foco=float(row.media_foco or 0.0),
            media_energia=float(row.media_energia or 0.0),
            tempo_total_focado=int(row.tempo_total_focado or 0),
            taxa_uso_ia=float((sessoes_com_ia / total_sessoes) * 100.0),
            indice_esgotamento=float(soma_esgotamento / total_sessoes),
            total_sessoes=total_sessoes
        )

