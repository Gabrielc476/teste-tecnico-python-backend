# Contexto do Projeto: API de Log de Performance e Foco (Foco em TDAH, Simbiose com IA e Zero Fricção)

## 1. Visão Geral
Você é um desenvolvedor Sênior Python construindo uma solução de "Log de Performance" dividida em duas partes: um **Backend (API)** e um **Client Desktop (Zero Fricção)**. O objetivo é medir o estado de fluxo (flow) com adaptações para auxiliar pessoas com TDAH, medindo o custo energético do foco e o ganho de produtividade ao utilizar ferramentas de IA. A entrada de dados deve ter fricção mínima.

## 2. Diretrizes de Arquitetura e Engenharia
- **Linguagem/Framework:** Python 3.x. Backend em FastAPI e Client usando bibliotecas nativas (`tkinter`, `keyboard`).
- **Princípios:** Aplique estritamente Clean Architecture, SOLID e Clean Code no Backend.
- **Estrutura do Repositório:** O código deve ser dividido claramente em duas pastas principais:
  - `/api`: Contém o Domínio, Casos de Uso e Infraestrutura (FastAPI, SQLite).
  - `/client`: Contém o script de atalho global em background.

## 3. Especificações do Client Desktop (Zero Fricção)
- **Gatilho:** Um atalho global de teclado (ex: `Ctrl + Shift + F`) para iniciar e parar o timer da sessão de foco silenciosamente em background.
- **Interface:** Ao encerrar a sessão, exibe uma janela minimalista nativa (`tkinter`) sobrepondo a IDE.
- **Coleta:** Pede apenas `nivel_foco` (1-5, slider), `nivel_energia` (1-5, slider) e `ia_auxiliou` (checkbox). O `tempo_minutos` é calculado automaticamente pelo client.
- **Comunicação:** Ao confirmar, envia o payload via `requests.post` para a API e fecha a janela imediatamente.

## 4. Entidades de Domínio (Backend)

### Registro de Foco (FocusLog)
- `id`: UUID.
- `nivel_foco`: Inteiro (1 a 5).
- `nivel_energia`: Inteiro (1 a 5) -> *Métrica para medir esgotamento cognitivo*.
- `tempo_minutos`: Inteiro (Recebido do client).
- `comentario`: String -> *O que foi feito ou o que causou distração (Obrigatório)*.
- `ia_auxiliou`: Booleano.
- `categoria`: String -> *Opcional (ex: coding, reunião, estudo)*.
- `data_registro`: DateTime.

## 5. Endpoints Exigidos (Backend)

### 5.1. POST /registro-foco
- Recebe os dados do bloco de trabalho enviados pelo Client Desktop.
- Valida estritamente usando Pydantic se `nivel_foco` e `nivel_energia` estão entre 1 e 5.
- Persiste os dados no SQLite (via injeção de dependência do repositório).

### 5.2. GET /diagnostico-produtividade
Retorna um resumo analítico de todas as sessões. Deve processar as regras de negócio de TDAH e IA para gerar feedbacks gamificados.
O JSON de resposta deve conter:
- `media_foco`: Float.
- `tempo_total_focado`: Inteiro (minutos).
- `indice_esgotamento`: Float (Média da diferença entre Foco e Energia. Se Foco é alto e Energia é baixa, o custo cognitivo foi alto).
- `taxa_uso_ia`: Porcentagem das sessões onde a IA auxiliou.
- `mensagem_feedback`: String gerada baseada em status gamificados. Exemplos de regras:
  - Se `Energia < 2` e `Foco > 4`: "Status: Hiperfoco Exaustivo. Sua mana está no fim. Faça um 'Descanso Curto' antes da próxima task, ou rolará com desvantagem na atenção."
  - Se `ia_auxiliou` for alto e `tempo_minutos` médio/baixo: "Buff Ativo: Simbiose Mágica. A IA agiu como um excelente familiar, acelerando entregas sem drenar sua bateria."
  - Se `media_foco` e `nivel_energia` estiverem equilibrados: "Condição ideal. Você manteve um ritmo sustentável sem sacrificar seus pontos de vida."

## 6. Instruções de Execução para a IA
1. Crie a estrutura de pastas separando `/api` e `/client`.
2. Implemente o `/client/tracker.py` usando `keyboard` e `tkinter`.
3. No Backend (`/api`), inicie criando as Entidades de Domínio e as Interfaces de Repositório.
4. Implemente os Casos de Uso (Use Cases), utilizando o Design Pattern *Strategy* para as regras de geração da `mensagem_feedback`.
5. Finalize com a camada de Infraestrutura (FastAPI Routers e SQLAlchemy/SQLite).
6. Mantenha os métodos curtos, descritivos e tipe todos os parâmetros e retornos (Type Hints).