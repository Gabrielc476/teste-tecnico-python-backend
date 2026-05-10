# Wiki do Projeto: API de Log de Performance e Foco (TDAH)

## 📌 Visão Geral
Sistema de log de performance focado em desenvolvedores e estudantes com TDAH. O objetivo principal é minimizar a fricção de entrada e gerar diagnósticos inteligentes sobre o "estado de fluxo" (flow) e o "burnout cognitivo", gamificando a produtividade.

## 🏗 Arquitetura e Estrutura de Pastas
O projeto adota Clean Architecture e está estruturado da seguinte forma:

```text
c:\projetos\desafio sou junior\
├── .venv/                # Ambiente virtual Python
├── .env                  # Variáveis de ambiente (DATABASE_URL) — não versionado
├── .env.example          # Template de variáveis de ambiente para novos devs
├── api/                  # Backend FastAPI
│   ├── __init__.py       # Inicializador do pacote api
│   ├── domain/           # Entidades e Regras de Negócio (Isolado, Python puro)
│   │   ├── __init__.py   # Inicializador do pacote domain
│   │   ├── entities.py   # Dataclasses de domínio (FocusLog)
│   │   ├── ports.py      # Interfaces/ABC de repositório (inversão de dependência)
│   │   ├── metrics.py    # Calculadora de métricas de produtividade e esgotamento
│   │   └── strategies.py # Matriz de estratégias de feedback (Strategy Pattern)
│   ├── usecases/         # Casos de uso da aplicação (Orquestração)
│   ├── infrastructure/   # Camada externa: FastAPI, SQLModel/SQLite, DI
│   │   ├── database.py   # Engine e Session factory (SQLModel + .env)
│   │   ├── models.py     # Modelo ORM FocusLogModel (SQLModel, table=True)
│   │   ├── repository.py # SQLiteFocusLogRepository (implementa ports.py)
│   │   ├── container.py  # Container de Injeção de Dependência (Depends)
│   │   ├── schemas.py    # Schemas Pydantic de request/response
│   │   └── routes.py     # Rotas/Controllers do FastAPI
│   └── main.py           # Ponto de entrada da API
├── client/               # Client Desktop Resiliente (TDAH-Friendly)
│   └── tracker.py        # Script em background (pystray + customtkinter)
├── docs/                 # Documentação e README oficial
│   └── README.md
├── ai_artifacts/         # Artefatos auxiliares de IA e especificações
│   ├── wiki.md
│   ├── agents.md
│   └── logica_de_calculo.md
├── requirements.txt      # Dependências do projeto
└── .gitignore            # Exclusões do controle de versão
```

1. **Client Desktop (`/client`)**: 
   - Script rodando silenciosamente com ícone de controle na Bandeja do Sistema (System Tray).
   - Usa interface moderna e minimalista (`customtkinter`) para coleta super rápida de métricas no fim da sessão, além de persistência offline.
2. **Backend API (`/api`)**: 
   - API construída com **FastAPI** + **SQLModel** (ORM que unifica SQLAlchemy + Pydantic).
   - Responsável por persistir os logs de foco usando **SQLite** (URL configurada via `.env`).
   - Processa os dados brutos para entregar um diagnóstico de produtividade refinado.

## 🧮 Métricas Base e Cálculos
As métricas derivam dos registros (`FocusLog`), que armazenam:
- Nível de Foco e Nível de Energia (Escala de 1-5)
- Tempo em minutos (calculado pelo client)
- Comentário (String descrevendo a sessão ou distração)
- Uso de Inteligência Artificial (Booleano)
- Categoria (Opcional: coding, reunião, estudo, etc.)

**As fórmulas calculadas incluem:**
- **Índice de Esgotamento**: Média da diferença matemática onde Foco > Energia. Quanto maior a discrepância, maior o custo cognitivo pago pelo usuário.
- **Taxa de Uso de IA (%)**: Sessões com auxílio de IA em relação ao total de sessões.

## 📋 Sistema de Diagnóstico (Matriz de Feedback)
Implementado usando o **Design Pattern Strategy**, as regras de negócio avaliam as métricas de forma sequencial e priorizada, retornando diagnósticos de foco focados e profissionais:
1. **Hiperfoco Exaustivo**: Nível de foco excelente associado a um alto esgotamento cognitivo. Recomenda repouso para evitar cansaço extremo.
2. **Simbiose com IA**: Uso produtivo e frequente de assistentes de IA ajudando a otimizar as entregas e poupar estamina mental.
3. **Neblina Mental**: Nível de foco persistentemente baixo. Sugere quebras de rotina, beber água ou dividir tarefas grandes em micro-metas.
4. **Fluxo Sustentável**: Equilíbrio ideal entre boa produtividade e energia estável, permitindo foco saudável a longo prazo.

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.10 ou superior instalado.

### Configuração do Ambiente
1. Ative o ambiente virtual:
   - **PowerShell:** `.venv\Scripts\Activate.ps1`
   - **CMD:** `.venv\Scripts\activate.bat`
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure as variáveis de ambiente:
   ```bash
   cp .env.example .env
   ```
   O arquivo `.env` já vem com o valor padrão `DATABASE_URL=sqlite:///./api/infrastructure/focus.db`.

### Execução
- **Iniciar a API (Backend):**
  ```bash
  uvicorn api.main:app --reload
  ```
  Acesse a documentação interativa em `http://127.0.0.1:8000/docs` ou o health-check em `http://127.0.0.1:8000/health`.

- **Iniciar o Monitor (Client Desktop):**
  ```bash
  python client/tracker.py
  ```

---
*Para detalhes matemáticos de implementação, consulte a `logica_de_calculo.md`.*
