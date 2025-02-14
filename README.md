# Cotação do Bitcoin com Gráfico Histórico

Este é um projeto simples em Python que exibe a cotação atual do Bitcoin e um gráfico histórico da variação do preço. A interface gráfica foi desenvolvida usando `tkinter`, e os dados são obtidos da API do [CoinGecko](https://www.coingecko.com/).

## Funcionalidades Implementadas

1. **Cotação Atual**:
   - Exibe o preço atual do Bitcoin em dólares (USD).

2. **Gráfico Histórico**:
   - Mostra a variação do preço do Bitcoin nos últimos 7 dias, 30 dias ou 1 ano.
   - O gráfico é atualizado automaticamente a cada 30 segundos.

3. **Seleção de Período**:
   - O usuário pode escolher entre diferentes períodos para visualizar o gráfico:
     - Tempo Real (últimas 24 horas)
     - 7 Dias
     - 30 Dias
     - 1 Ano


### Pré-requisitos

- Python 3.x instalado.
- Bibliotecas necessárias: `requests`, `matplotlib`, `tkinter`.
