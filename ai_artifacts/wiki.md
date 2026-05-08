# Wiki do Projeto: API de Log de Performance e Foco (TDAH)

## 📌 Visão Geral
Sistema de log de performance focado em desenvolvedores e estudantes com TDAH. O objetivo principal é minimizar a fricção de entrada e gerar diagnósticos inteligentes sobre o "estado de fluxo" (flow) e o "burnout cognitivo", gamificando a produtividade.

## 🏗 Arquitetura
O projeto adota Clean Architecture e é dividido em duas partes principais:
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

## 🎮 Sistema de Diagnóstico (Matriz de Feedback)
Implementado usando o **Design Pattern Strategy**, as regras de negócio avaliam as métricas e retornam "Status" RPGísticos:
1. **Hiperfoco Exaustivo (Debuff)**: Foco muito alto enquanto a energia está muito baixa. Alerta para a "mana no fim".
2. **Simbiose Mágica (Buff)**: Alta utilização de IA resultando em preservação da energia vital.
3. **Neblina Mental (Debuff)**: Foco consistentemente baixo. Sugere quebras de rotina ou hidratação.
4. **Fluxo Sustentável (Condição Ideal)**: Manutenção perfeita e equilibrada entre as barras de energia e foco.

---
*Para detalhes matemáticos de implementação, consulte a `logica_de_calculo.md`.*
