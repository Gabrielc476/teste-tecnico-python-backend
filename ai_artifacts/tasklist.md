# Checklist de Implementação: Foco TDAH (API e Client Desktop)

Este documento rastreia o progresso do desenvolvimento do projeto do zero à entrega.

## Fase 1: Setup e Infraestrutura
- [x] Criar a estrutura base de diretórios (`/api`, `/client`, `/docs`).
- [x] Configurar os arquivos `requirements.txt` (FastAPI, Pydantic, SQLAlchemy, Uvicorn, Requests, Keyboard).
- [x] Configurar um `main.py` inicial no backend que rode o FastAPI com um endpoint de health-check simples.

## Fase 2: Domínio e Regras de Negócio (Backend)
- [x] Criar o modelo/entidade de domínio `FocusLog` usando Dataclasses.
- [x] Implementar a interface (Abstract Base Class) `FeedbackRule` do padrão Strategy.
- [x] Implementar as 5 regras de Strategy (ExhaustiveHyperfocusRule, MagicalSymbiosisRule, MentalFogRule, SustainableFlowRule, DefaultFeedbackRule).
- [x] Implementar a classe pura `MetricsCalculator` (fórmulas de índice de esgotamento e média).

## Fase 3: Casos de Uso (Backend)
- [x] Criar Interface `FocusLogRepository` para inversão de dependência (SOLID).
- [x] Criar Caso de Uso: `RegisterFocusSessionUseCase` (Valida a entrada e persiste os dados).
- [x] Criar Caso de Uso: `GenerateProductivityDiagnosticsUseCase` (Busca todos os logs, passa pelo `MetricsCalculator` e gera o status via Strategy).

## Fase 4: Banco de Dados e API (Backend)
- [x] Implementar a infraestrutura de Banco de Dados: `SQLiteFocusLogRepository` e modelos do SQLModel.
- [x] Configurar o Container de Injeção de Dependência.
- [x] Criar Rotas (Controllers) do FastAPI: `POST /registro-foco` usando os modelos SQLModel diretamente.
- [x] Criar Rotas (Controllers) do FastAPI: `GET /diagnostico-produtividade`.

## Fase 5: Client Desktop Zero Fricção
- [ ] Criar a classe principal do Tracker e a lógica de timer invisível no background usando `keyboard`.
- [ ] Criar a Interface Gráfica nativa Minimalista com `tkinter` que só aparece ao encerrar o log (Sliders de 1 a 5 e Checkbox de IA).
- [ ] Implementar a função de comunicação HTTP que faz o `POST /registro-foco` e limpa/encerra a tela.

## Fase 6: Testes, Polimento e Entrega
- [ ] Escrever testes unitários em PyTest para o `MetricsCalculator` e para os `Strategies` de Feedback.
- [ ] Testar integração end-to-end (Acionar atalho do teclado -> Submeter no tkinter -> Verificar se gravou no SQLite via GET na API).
- [ ] Adicionar e formatar o `README.md` final do projeto ensinando como executar a aplicação.
