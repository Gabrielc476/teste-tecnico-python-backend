# 🧠 Log de Foco e Performance (TDAH-Flow-Architect)

> Uma solução de alta performance desenvolvida para medir o estado de fluxo (*flow*), a simbiose com Inteligências Artificiais e o esgotamento cognitivo, adaptada especificamente com baixa fricção para pessoas com TDAH.

Este projeto adota **Clean Architecture** e **SOLID** estritos na construção de um Backend em **FastAPI** aliado a um **Client Desktop nativo e resiliente** (rodando na bandeja do sistema via `pystray` com pop-up moderno em `customtkinter`).

---

## 🏗 Arquitetura do Projeto

O código do backend é desenvolvido sob a filosofia de arquitetura limpa, isolando totalmente as regras de negócio de frameworks ou dependências externas.

```text
c:\projetos\desafio sou junior\
├── .venv/                 # Ambiente virtual isolado do Python
├── .env / .env.example    # Variáveis de ambiente (API_URL, DATABASE_URL)
├── api/                   # Backend FastAPI
│   ├── domain/            # Camada de Domínio (Python puro, acoplamento zero)
│   │   ├── entities.py    # Dataclasses de domínio e validações (Strategy Pattern simplificado)
│   │   ├── metrics.py     # Lógicas de cálculo (MetricsCalculator)
│   │   └── ports.py       # Interfaces de Inversão de Dependência (FocusLogRepository)
│   ├── usecases/          # Camada de Aplicação (orquestração do domínio)
│   ├── infrastructure/    # Adaptadores e Infraestrutura (SQLModel, SQLite, Injeção)
│   └── main.py            # Inicializador e rotas iniciais do FastAPI
├── client/                # Client Desktop Resiliente (TDAH-Friendly)
│   └── tracker.py         # Tracker via System Tray (pystray) e UI Moderna (customtkinter)
├── tests/                 # Testes Unitários e de Integração
├── docs/                  # Documentação do desafio técnico original
├── ai_artifacts/          # Artefatos e especificações de IA (wiki, checklists)
└── requirements.txt      # Dependências de execução
```

---

## 🧮 Lógica de Negócio e Métricas (Fase 2)

Na camada de domínio, toda a matemática e matriz de feedbacks foram estruturadas, parametrizadas e validadas:

*   **Eliminação de Magic Numbers (ClassVar):** Os limiares de controle de estamina mental não possuem valores numéricos soltos (*hardcoded*) no domínio. Toda a parametrização utiliza constantes de classe em [metrics.py](file:///c:/projetos/desafio%20sou%20junior/api/domain/metrics.py) através de `ClassVar[float]`, garantindo parametrização limpa e flexível.
*   **Índice de Esgotamento Cognitivo (Burnout Index):** Mede o real custo metabólico e cognitivo do foco. Pessoas com TDAH entram com frequência em estados de hiperfoco que drenam totalmente sua stamina. A fórmula é dada por:
    $$I_{esgotamento} = \frac{\sum_{i=1}^{N} \max(0, Foco_i - Energia_i)}{N}$$
*   **Design Simplificado de Strategy:** O padrão Strategy clássico foi simplificado e incorporado diretamente à lógica das entidades (`entities.py`), eliminando o excesso de engenharia (*over-engineering*) e mantendo a matriz de feedbacks eficiente e direta:
    1.  **Hiperfoco Exaustivo:** Foco excelente com alto esgotamento cognitivo.
    2.  **Simbiose com IA:** Identificação do uso eficiente de assistentes de IA para poupar energia mental.
    3.  **Neblina Mental:** Alerta para foco persistentemente baixo, instruindo micro-metas ou descanso físico.
    4.  **Fluxo Sustentável:** Estado ideal equilibrado de energia e atenção.
    5.  **Fallback (Default):** Retorno de feedback padrão encorajador.

---

## ⚙️ Casos de Uso e Inversão de Dependência (Fase 3)

A camada de aplicação isola a orquestração através do padrão **Ports & Adapters**:
*   **Portas de Repositório:** A interface `FocusLogRepository` abstrai o banco de dados. Os casos de uso não conhecem detalhes de infraestrutura.
*   **Casos de Uso (Use Cases):** `RegisterFocusSessionUseCase` e `GenerateProductivityDiagnosticsUseCase` orquestram o domínio de forma testável e independente.
*   **Contexto Rico e Retrocompatibilidade:** Suporte aos campos `comentario` (obrigatório) e `categoria` (opcional). Campos como `nivel_energia` e `ia_auxiliou` foram flexibilizados como opcionais para facilitar o envio do payload, mantendo a compatibilidade estrita do desafio.

---

## 🗄️ Banco de Dados e API FastAPI (Fase 4)

A infraestrutura foi construída sob a base sólida do **FastAPI** e **SQLModel**:
*   **Banco de Dados Embutido:** Utilização do SQLite (`database.py`) para garantir um setup *plug-and-play* sem configurações externas.
*   **Otimização com SQL Nativo:** Os cálculos de métricas agregadas (como média de foco, total de sessões, esgotamento, etc.) são realizados de forma otimizada através do próprio SQL direto no banco de dados (`repository.py`), reduzindo a carga em memória e aumentando a performance.
*   **Injeção de Dependência (DI):** Uso do `Depends` do FastAPI (`container.py`) para injetar repositórios nos casos de uso, garantindo isolamento total.
*   **Endpoints Restful:** Rotas puras (`POST /registro-foco` e `GET /diagnostico-produtividade`) desacopladas das regras de negócio.

---

## 🖥️ Client Desktop Resiliente (Fase 5)

O Client Desktop nativo em [tracker.py](file:///c:/projetos/desafio%20sou%20junior/client/tracker.py) (construído com `pystray` e `customtkinter`) foi projetado para rodar na bandeja do sistema de forma thread-safe e configurável:

*   **Bloqueio Atômico de I/O (`FILE_LOCK`):** Para evitar condições de corrida (Race Conditions) ao manipular a sessão ativa (`.current_session.json`) ou a fila de sincronização offline (`offline_queue.json`) a partir de diferentes threads em segundo plano, todas as operações de leitura, gravação e exclusão são protegidas por um bloqueio atômico de exclusão mútua (`threading.Lock`).
*   **Variáveis de Ambiente (`.env`):** A URL de comunicação da API não é hardcoded no código do tracker. Ela é carregada de forma dinâmica utilizando `python-dotenv` através do parâmetro `API_URL` com fallback limpo.
*   **Falha Graciosa:** Tratamento de erros detalhado e específico (ex: `json.JSONDecodeError`, `OSError`), garantindo que falhas em rede ou de leitura de arquivos corrompidos não causem crash no client.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
*   Python 3.10 ou superior.

### Passo 1: Configuração e Ativação do Ambiente
No terminal (dentro do diretório raiz), execute:

```bash
# Ativar o ambiente virtual (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Ou no CMD clássico do Windows
.venv\Scripts\activate.bat
```

### Passo 2: Instalar Dependências
```bash
pip install -r requirements.txt
```

### Passo 3: Iniciar o Servidor de Desenvolvimento
```bash
uvicorn api.main:app --reload
```
A API estará disponível em `http://127.0.0.1:8000`. Acesse a documentação interativa através de `http://127.0.0.1:8000/docs` ou verifique se está no ar acessando o health-check `/health`.

### Passo 4: Iniciar o Client Desktop
Em um novo terminal com o ambiente virtual ativado, rode:
```bash
python client/tracker.py
```
Um ícone aparecerá na Bandeja do Sistema (área de notificação do Windows). Clique com o botão direito sobre ele para iniciar e parar suas sessões de foco.

---

## 🧪 Rodando os Testes Unitários

Os testes validam o comportamento matemático das métricas, as regras de priorização de feedbacks e os casos de uso de registro e diagnóstico. Para executá-los:

```bash
python -m unittest discover tests -v
```

