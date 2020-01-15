import logging
import os
import datetime

from utils import *
from instance import *
from crawler import *
from user import *

import seleniumrequests
from selenium import webdriver
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
from telegram import ForceReply

user = User()
token = os.environ["API_TOKEN"]
data = list()
alive = False
id_list = [650172463,1066700692]
last_update = ""

logging.basicConfig(
    format="%(asctime)s - %(levelname)s -> %(message)s", level=logging.INFO, datefmt='%d/%m %H:%M:%S'
)
logger = logging.getLogger(__name__)

updater = Updater(token)


def start(bot, update, job_queue):
    global data, user, alive, last_update
    """Send a message when the command /start is issued."""
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Olá, eu sou o bot assistente da Artivinco.\nDigite /ajuda para listar meus comandos!",
    )
    if not alive:
        alive = True
        first_load()
        last_update = datetime.now() - timedelta(hours=2)
        job_queue.run_repeating(
                update_billing, interval=1200, first=2, context=update.message
        )
    bot.send_message(chat_id=update.message.chat_id,text=update.message.from_user.first_name+", tudo pronto!")


def help(bot, update):
    """Send a message when the command /ajuda is issued."""
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Segue lista com meus comandos\n\n" +
        "pedido número_do_pedido - Informa dados de um pedido especifico" +
        "expedição - Informa os dados de todos os pedidos em expedição" +
        "programado - Informa os dados de todos os pedidos programados"
    )


def status(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Informe o número do pedido",
        reply_markup=ForceReply(),
    )
    status_attr(bot, update)

def test(bot, update):
        global data, last_update
        cmd = update.message.text.split()[1]
        if cmd == "dump_id":
                bot.send_message(
                        chat_id = update.message.chat_id,
                        text= "; ".join([ ID_TO_NAME[idx]+":"+str(idx) for idx in id_list])
                )
        elif cmd == "data_size":
                bot.send_message(
                        chat_id = update.message.chat_id,
                        text= str(len(data))
                )
        elif cmd == "last_update":
                bot.send_message(
                        chat_id = update.message.chat_id,
                        text= last_update.strftime("%m/%d/%Y, %H:%M:%S")
                )
        elif cmd == "reload_data":
                data.clear()
                data = load_from_csv("report")
                bot.send_message(
                        chat_id = update.message.chat_id,
                        text= "Done"
                )
        elif cmd == "help":
                bot.send_message(
                        chat_id = update.message.chat_id,
                        text= "dump_id, data_size"
                )

def update_billing(bot, job):
    global data, user, id_list, last_update
    options = webdriver.ChromeOptions()
    # options.binary_location = os.environ["GOOGLE_CHROME_BIN"]
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    browser = seleniumrequests.Chrome(executable_path=os.environ["CHROMEDRIVER_PATH"], chrome_options=options)
    browser.implicitly_wait(60)
    logger.info(job.context.from_user.first_name + " - Iniciando crawler")
    crawler = Crawler(browser, user)
    crawler.run()
    logger.info(job.context.from_user.first_name + " - Iniciando parse")
    export_to_csv("report", crawler.table)
    browser.quit()
    data, updates = update_from_csv("report", data)
    last_update = datetime.now() - timedelta(hours=2)
    logger.info(job.context.from_user.first_name + " - Checkando e notificando atualizações")
    if len(updates):
        for update in updates:
                for chat_id in id_list:
                        if update.auth(chat_id):
                                logger.info(ID_TO_NAME[chat_id] + " - Pedido Nº" + update.data["Pedido"])
                                bot.send_message(chat_id=chat_id, text=str(update))

def first_load():
    global data, user
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ["GOOGLE_CHROME_BIN"]
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    browser = seleniumrequests.Chrome(executable_path=os.environ["CHROMEDRIVER_PATH"], chrome_options=options)
    browser.implicitly_wait(60)
    logger.info("Iniciando crawler (first load)")
    crawler = Crawler(browser, user)
    crawler.run()
    logger.info("Iniciando parse (first load)")
    export_to_csv("report", crawler.table)
    browser.quit()
    data, updates = update_from_csv("report", data)
    last_update = datetime.now() - timedelta(hours=2)


def noncommand(bot, update):
    global data
    infos = -1
    text = (update.message.text).lower().replace("ç","c").replace("ã","a")
    if text.isdigit() or "pedido" in text:
        if "pedido" in text:
                pedido = text.split()[1]
        else:
                pedido = text
        log = update.message.from_user.first_name + " - Nova consulta - Pedido Nº " + pedido
        infos = query(data=data, q_id=update.message.chat_id, q_n=pedido, q_type="pedido")
        if infos == -1:
            log += " - Invalido"
        logger.info(log)

    elif text == "expedicao":
        log = update.message.from_user.first_name + " - Nova consulta - Expedição"
        logger.info(log)
        infos = query(data=data, q_id=update.message.chat_id, q_type="expedicao")

    elif text == "programado":
        log = update.message.from_user.first_name + " - Nova consulta - Programado"
        logger.info(log)
        infos = query(data=data, q_id=update.message.chat_id, q_type="programado")

    if infos != -1:
        for info in infos:
                bot.send_message(chat_id=update.message.chat_id, text=str(info))
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Consulta inválida")


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
    dp.add_handler(CommandHandler("ajuda", help ))
    dp.add_handler(CommandHandler("test", test))

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


if __name__ == "__main__":
    main()
