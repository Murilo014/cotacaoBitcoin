from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

# Função para obter a cotação do Bitcoin
def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data['bitcoin']['usd']

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Olá! Use o comando /btc para obter a cotação atual do Bitcoin.')

# Comando /btc
async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_btc_price()
    await update.message.reply_text(f'A cotação atual do Bitcoin é: ${price}')

# Função principal
def main() -> None:
    # Substitua 'SEU_TOKEN_AQUI' pelo token que você recebeu do BotFather
    application = Application.builder().token("7914280340:AAH2A_maA-PwRzNyh_c1lfyhbOxVXpZjBeM").build()

    # Adiciona os comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("btc", btc))

    # Inicia o bot
    application.run_polling()

if __name__ == '__main__':
    main()