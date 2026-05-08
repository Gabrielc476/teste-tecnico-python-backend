# 🧠 Log de Foco e Performance (TDAH-Flow-Architect)

> Uma solução de alta performance desenvolvida para medir o estado de fluxo (*flow*), a simbiose com Inteligências Artificiais e o esgotamento cognitivo, adaptada especificamente com baixa fricção para pessoas com TDAH.

Este projeto adota **Clean Architecture** e **SOLID** estritos na construção de um Backend em **FastAPI** aliado a um **Client Desktop nativo de Zero Fricção** (com atalhos globais de teclado e pop-up rápido em Tkinter).

---

## 🏗 Arquitetura do Projeto

O código do backend é desenvolvido sob a filosofia de arquitetura limpa, isolando totalmente as regras de negócio de frameworks ou dependências externas.

```text
c:\projetos\desafio sou junior\
├── .vscode/               # Configurações de ambiente para VS Code
├── .venv/                 # Ambiente virtual isolado do Python
├── api/                   # Backend FastAPI
│   ├── domain/            # Camada de Domínio (Python puro, acoplamento zero)
│   │   ├── entities.py    # Dataclasses de domínio (ex: FocusLog)
│   │   ├── metrics.py     # Lógicas de cálculo puro (MetricsCalculator)
│   │   └── strategies.py  # Regras de diagnósticos gamificados (Strategy Pattern)
│   └── main.py            # Inicializador e rotas iniciais do FastAPI
├── client/                # Client Desktop de Zero Fricção
│   └── tracker.py         # Script em background em Tkinter e keyboard (placeholder)
├── docs/                  # Documentação do desafio técnico original
├── ai_artifacts/          # Artefatos e especificações de IA (wiki, checklists)
└── requirements.txt      # Dependências de execução
```

---

## 🧮 Lógica de Negócio e Métricas (Fase 2)

Na camada de domínio, toda a matemática e matriz de feedbacks foram estruturadas e validadas:

*   **Índice de Esgotamento Cognitivo (Burnout Index):** Mede o real custo metabólico e cognitivo do foco. Pessoas com TDAH entram com frequência em estados de hiperfoco que drenam totalmente sua stamina. A fórmula é dada por:
    $$I_{esgotamento} = \frac{\sum_{i=1}^{N} \max(0, Foco_i - Energia_i)}{N}$$
*   **Padrão Strategy (Matriz de Feedbacks):** As regras de diagnóstico inteligentes avaliam as sessões de foco em ordem de prioridade estrita, gerando relatórios precisos sem termos punitivos ou jargões lúdicos excessivos:
    1.  **Hiperfoco Exaustivo:** Foco excelente com alto esgotamento cognitivo.
    2.  **Simbiose com IA:** Identificação do uso eficiente de assistentes de IA para poupar energia mental.
    3.  **Neblina Mental:** Alerta para foco persistentemente baixo, instruindo micro-metas ou descanso físico.
    4.  **Fluxo Sustentável:** Estado ideal equilibrado de energia e atenção.
    5.  **Fallback (Default):** Retorno de feedback padrão encorajador.

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

---

## 🧪 Rodando os Testes Unitários

Os testes validam o comportamento matemático das métricas, as regras de priorização de feedbacks e os casos de uso de registro e diagnóstico. Para executá-los:

```bash
python -m unittest tests/test_usecases.py -v
```

