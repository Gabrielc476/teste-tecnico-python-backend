# Lógica de Medições e Regras de Diagnóstico

Este documento define as fórmulas matemáticas e as regras de negócio (feedbacks) que devem ser implementadas no endpoint `GET /diagnostico-produtividade`. A lógica deve ser implementada na camada de Domínio, seguindo o padrão Strategy para garantir que novas regras possam ser adicionadas sem modificar as existentes.

## 1. Entradas Esperadas (Base de Cálculo)
Todos os cálculos derivam de uma lista de registros de foco (`FocusLog`), onde cada registro contém:
- `nivel_foco` (1 a 5)
- `nivel_energia` (1 a 5)
- `tempo_minutos` (Inteiro)
- `ia_auxiliou` (Booleano)

## 2. Fórmulas das Métricas Principais

### A. Média de Foco e Energia
Cálculo aritmético simples. Soma-se o valor de todos os registros e divide-se pelo total de sessões.

### B. Índice de Esgotamento Cognitivo (Burnout Index)
Mede o custo energético do foco. Se o usuário foca muito, mas a energia cai drasticamente, o custo foi muito alto (comportamento típico do hiperfoco no TDAH).
Para cada sessão, calculamos a diferença entre Foco e Energia (apenas se o foco for maior que a energia). A fórmula matemática para a média final é:

$$I_{esgotamento} = \frac{\sum_{i=1}^{N} \max(0, Foco_i - Energia_i)}{N}$$

Onde $N$ é o número total de registros.

### C. Taxa de Uso de IA (%)
Mede a frequência com que a IA atuou como auxiliar de desenvolvimento nas sessões de foco.
- **Fórmula:** `(Sessões_com_IA / Total_Sessões) * 100`

## 3. Matriz de Feedbacks (Regras de Negócio)
O gerador de diagnóstico deve avaliar as métricas calculadas acima contra as seguintes regras, em ordem de prioridade. A primeira regra que retornar verdadeira definirá a `mensagem_feedback` da resposta.

### Regra 1: Hiperfoco Exaustivo (Debuff)
- **Condição:** `indice_esgotamento >= 2.0` E `media_foco >= 4.0`
- **Mensagem:** "Status: Hiperfoco Exaustivo. Sua mana está no fim. Hora de fazer um 'Descanso Curto' ou você vai rolar com desvantagem na atenção no próximo bloco."

### Regra 2: Simbiose Mágica com IA (Buff)
- **Condição:** `taxa_uso_ia >= 50.0%` E `media_energia >= 3.0`
- **Mensagem:** "Buff Ativo: Simbiose Mágica. A IA serviu como um excelente familiar, acelerando suas entregas sem drenar sua bateria mental."

### Regra 3: Neblina Mental (Debuff)
- **Condição:** `media_foco < 2.5`
- **Mensagem:** "Debuff: Neblina Mental. Foco baixo detectado. Considere mudar de ambiente, beber água ou dividir a próxima tarefa em pedaços menores (micro-vitórias)."

### Regra 4: Fluxo Sustentável (Condição Ideal)
- **Condição:** `media_foco` entre `3.0` e `4.5` E `media_energia >= 3.5`
- **Mensagem:** "Condição Ideal: Fluxo Sustentável. Você manteve um ritmo constante sem sacrificar seus pontos de vida. Excelente gestão de estamina."

### Regra Default (Fallback)
- **Condição:** Nenhuma das acima.
- **Mensagem:** "Sessão registrada. Continue monitorando seus atributos para descobrirmos seu padrão de produtividade."

## 4. Instruções de Implementação
- Crie uma classe pura `MetricsCalculator` para as fórmulas.
- Crie uma interface `FeedbackRule` com um método `evaluate(metrics)`.
- Implemente cada regra da Matriz de Feedbacks como uma classe separada herdando de `FeedbackRule`.