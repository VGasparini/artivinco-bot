from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
from telegram import ForceReply
from bot_utils import *
import logging
import os
import datetime

token = read_token()
logged = False
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
updater = Updater(token)
j = updater.job_queue
data,cont = list(),0

def first_load_csv():
        global data
        with open('report.csv', mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                to_return = ''
                fields = ['Representante','Cliente','Data','Referência','Pedido']
                for row in csv_reader:
                        for header in row.keys():
                                if header == None:
                                                headers = row.keys()
                                                instance = dict()
                                                for header in headers:
                                                        if header == None:
                                                                if row[header][0] != '':
                                                                        instance['nf'] = row[header][0]
                                                                else:
                                                                        instance['nf'] = False
                                                                instance['status'] = row[header][1]
                                                        if header in fields:
                                                                instance[header.lower()] = row[header]
                                                logger.info(convert_to_string(instance))
                                                data.append(instance)
                                                del instance


def verify_update():
        global data
        with open('report.csv', mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                to_return = ''
                fields = ['Representante','Cliente','Data','Referência','Pedido']
                for row in csv_reader:
                        for header in row.keys():
                                instance = dict()
                                if header == None:
                                        if row[header][0] != '':
                                                headers = row.keys()
                                                for header in headers:
                                                        if header == None:
                                                                if row[header][0] != '':
                                                                        instance['nf'] = row[header][0]
                                                                else:
                                                                        instance['nf'] = False
                                                                instance['status'] = row[header][1]
                                                        if header in fields:
                                                                instance[header.lower()] = row[header]
                                if instance not in data and len(instance):
                                        data.append(instance)
                                        to_return += convert_to_string(instance)
                                        logger.info(''.join(['Nova atualização -',instance['cliente'], ' - NF ', instance['nf']]))
                                del instance
        if to_return:
                return to_return

def start(bot, update, job_queue):
        """Send a message when the command /start is issued."""
        bot.send_message(chat_id=update.message.chat_id,
                        text='Olá, eu sou o bot assistente da Artivinco.\nDigite /ajuda para listar meus comandos!')
        first_load_csv()
        bot.send_message(chat_id=update.message.chat_id,
                        text=convert_to_string(data[0]))
        job_queue.run_repeating(update_billing, interval=3600, first=2, context=update.message.chat_id)


def help(bot, update):
        """Send a message when the command /ajuda is issued."""
        bot.send_message(chat_id=update.message.chat_id,
                        text='Segue lista com meus comandos\n\n' +
                        '/atualizar - Recebe atualizações periodicas de faturamento\n' +
                        'nf número_da_nf - Informa dados de faturamento de uma nota fiscal especifica\n' +
                        'pedido número_do_pedido - Informa dados de de um pedido especifico')


def status(bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                        text='Informe a NF ou o número do pedido',
                        reply_markup=ForceReply())
        status_attr(bot, update)


def status_attr(bot, update):
        text = update.message.text
        bot.send_message(chat_id=update.message.chat_id,
                         text=verify_attr('nf',text, data))

# def login(bot, update):
#         text = update.message.text.split()
#         credencial = {}
#         credencial['username'] = text[1]
#         credencial['pass'] = text[2]
#         with open('credential.json', 'w') as f:
#                 json.dump(credencial, f)
#         update_billing(bot, update)
#         logged = True
        

# def logout(bot, update):
#         bot.send_message(chat_id=update.message.chat_id,
#                          text='Cancelado atualizações periodicas.\nPara ativar novamente digite /login email senha.')
#         logged = False


def update_billing(bot, job):
        global cont
        cont+=1
        if cont>4:
                logger.info("Sistema atualizado 5x")
                cont=0
        os.system('python3 update_faturamento.py')
        updates = verify_update()
        if updates:
                bot.send_message(chat_id=job.context,
                                text=updates)


def noncommand(bot, update):
        text = (update.message.text).lower()
        if 'nf' in text:
                nf = text.split()[1]
                info = verify_attr('nf',nf, data)
                log = (''.join(['Nova consulta - NF ', nf]))
                if(info=='Informação inválida'):
                        log += ' - Invalido'
                logger.info(log)
        elif 'pedido' in text :
                pedido = text.split()[1]
                info = verify_attr('pedido',pedido, data)
                log = (''.join(['Nova consulta - Pedido Nº', pedido]))
                if(info=='Informação inválida'):
                        log += ' - Invalido'
                logger.info(log)
        else:
                info = 'Comando inválido {}\n\nTente por:\nnf número da nota fiscal\npedido número do pedido'.format(text.lower())
        update.message.reply_text(info)


def error(bot, update, error):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, error)


def main():
        """Start the bot."""
        # Create the EventHandler and pass it your bot's token.
         # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("start", start, pass_job_queue=True))
        dp.add_handler(CommandHandler("ajuda", help))
        # dp.add_handler(CommandHandler("login", login))
        # dp.add_handler(CommandHandler("logout", logout))
        # dp.add_handler(CommandHandler("status", status))
        dp.add_handler(CommandHandler("atualizar", update_billing))

        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.text, noncommand))

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
