# Wiki do Projeto: API de Log de Performance e Foco (TDAH)

## 📌 Visão Geral
Sistema de log de performance focado em desenvolvedores e estudantes com TDAH. O objetivo principal é minimizar a fricção de entrada e gerar diagnósticos inteligentes sobre o "estado de fluxo" (flow) e o "burnout cognitivo", gamificando a produtividade.

## 🏗 Arquitetura e Estrutura de Pastas
O projeto adota Clean Architecture e está estruturado da seguinte forma:

```text
c:\projetos\desafio sou junior\
├── .venv/                # Ambiente virtual Python
├── api/                  # Backend FastAPI
│   ├── domain/           # Entidades e Regras de Negócio (Isolado)
│   │   ├── entities.py   # Dataclasses de domínio (FocusLog)
│   │   ├── metrics.py    # Calculadora de métricas de produtividade e esgotamento
│   │   └── strategies.py # Matriz de estratégias de feedback profissional
│   ├── usecases/         # Casos de uso da aplicação (Orquestração)
│   ├── infrastructure/   # Controladores FastAPI e Persistência SQLite
│   └── main.py           # Ponto de entrada da API
├── client/               # Client Desktop Zero Fricção
│   └── tracker.py        # Script em background (Tkinter + keyboard)
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
   - Script rodando em background com gatilhos de teclado silenciosos (ex: `Ctrl+Shift+F`).
   - Usa interface nativa e minimalista (`tkinter`) para coleta super rápida de métricas no fim da sessão.
2. **Backend API (`/api`)**: 
   - API construída com **FastAPI**.
   - Responsável por persistir os logs de foco usando SQLite.
   - Processa os dados brutos para entregar um diagnóstico de produtividade refinado.

## 🧮 Métricas Base e Cálculos
As métricas derivam dos registros (`FocusLog`), que armazenam:
- Nível de Foco e Nível de Energia (Escala de 1-5)
- Uso de Inteligência Artificial (Booleano)
- Tempo em minutos (calculado pelo client)

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
