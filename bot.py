from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import json
import os

token = open("token", "r").read()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    """Send a message when the command /start is issued."""
    bot.send_message(chat_id=update.message.chat_id,
                     text='Olá, eu sou o Severino. Sou o bot assistente da Artivinco.\nDigite /help para listar meus comandos!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    bot.send_message(chat_id=update.message.chat_id,
                     text='Segue lista com meus comandos\n\n' +
                            '/cadastro - Realiza autenticação Artivinco\n'+
                            '/atualiza_faturamento - Atualiza status de faturamento\n'+
                            '/atualiza_expedicao - Atualiza status de expedição')


def cadastro(bot, update):
    texto = update.message.text.split()
    credencial = {}
    credencial['username'] = texto[1]
    credencial['pass'] = texto[2]
    with open('credential.json', 'w') as f:
        json.dump(credencial, f)

def atualiza_faturamento(bot, update):
    os.system('python3 update_faturamento.py')
    update.message.reply_text('Atualizado')

def atualiza_expedicao(bot, update):
    os.system('python3 update_expedicao.py')
    update.message.reply_text('Atualizado')

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater=Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("cadastro", cadastro))
    dp.add_handler(CommandHandler("atualiza_faturamento", atualiza_faturamento))
    dp.add_handler(CommandHandler("atualiza_expedicao", atualiza_expedicao))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
