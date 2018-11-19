from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import json
import os
import csv

def update_csv():
        with open('report.csv', mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)

                data = [[] for _ in range(6)]
                for row in csv_reader:
                        data[0].append(row["Cliente"])
                        data[1].append(row["Referência"])
                        data[2].append(row["Nota Fiscal: Número Nota Fiscal"])
                        data[3].append(row["Quantidade faturada/entregue"])
                        data[4].append(row["Nota Fiscal: Data e hora da emissão"])
                        data[5].append(False)

def str_pedido(data_pedido):
        st = ''
        for i in range(len(data[2])):
                if data[2][i] == data_pedido and not data[6][i]:
                        st+= ('\nCliente ' + data[1][i]
                        + '\nPedido ' + data[3][i]
                        + '\nProduto ' + data[4][i]
                        + '\nStatus ' + data[5][i] + '\n')
                        data[6][i] = True
        return st

token = open("token", "r").read()
logged = False
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
updater = Updater(token)
j = updater.job_queue


def start(bot, update):
    """Send a message when the command /start is issued."""
    bot.send_message(chat_id=update.message.chat_id,
                     text='Olá, eu sou o Severino. Sou o bot assistente da Artivinco.\nDigite /help para listar meus comandos!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    bot.send_message(chat_id=update.message.chat_id,
                     text='Segue lista com meus comandos\n\n' +
                     '/login - Realiza autenticação Artivinco (informar o email e senha espaçados)\n' +
                     '/logout - Cancela recebimento de notificações')


def status(bot, update):
    data_pedido = update.message.text.split()
    bot.send_message(chat_id=update.message.chat_id,
                     text=str_pedido(data_pedido[1]))


def login(bot, update):
        texto = update.message.text.split()
        credencial = {}
        credencial['username'] = texto[1]
        credencial['pass'] = texto[2]
        with open('credential.json', 'w') as f:
                json.dump(credencial, f)
        j.run_repeating(atualiza_faturamento, interval=7200, first=0)

def logout(bot, update):
        global logged
        logged = False
        bot.send_message(chat_id=update.message.chat_id,
                         text='Cancelado atualizações periodicas.\nPara ativar novamente digite /login email senha.')

def atualiza_faturamento(bot, job):
        os.system('python3 update_faturamento.py')
        bot.send_message(chat_id=update.message.chat_id,
                         text='Atualizado!')


def atualiza_expedicao(bot, update):
        os.system('python3 update_expedicao.py')
        update.message.reply_text('Atualizado')


def error(bot, update, error):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, error)


def main():
        """Start the bot."""
        # Create the EventHandler and pass it your bot's token.
         # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))
        dp.add_handler(CommandHandler("login", login))
        dp.add_handler(CommandHandler("logout", logout))
        dp.add_handler(CommandHandler("atualiza", atualiza_faturamento))

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
