from logging import getLogger
import psycopg2
import  subprocess
import sys
from telegram import Bot
from telegram import Update
from telegram import ReplyKeyboardRemove
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters

from sqlalchemy import create_engine, Table, MetaData
import time
from utils import debug_requests
name, occupation = "", ""
logger = getLogger(__name__)
TG_TOKEN = "1750475954:AAHuD-iDv49AJzWx9UHZUYa7gUYAVN2eNmo"
maxim = []
filename = ""
NAME, OCCUPATION, ID = range(3)
@debug_requests
def start_handler(bot: Bot, update: Update):
    # Спросить имя
    update.message.reply_text(
        'Введи своё имя чтобы продолжить:',
        reply_markup=ReplyKeyboardRemove(),
    )
    return NAME


@debug_requests
def name_handler(bot: Bot, update: Update, user_data: dict):
    # Получить имя
    user_data[NAME] = update.message.text
    logger.info('user_data: %s', user_data)
    update.message.reply_text(f'''
   Введите название курса чтобы продолжить:
   ''')
    # TODO: кнопки !
    return OCCUPATION


@debug_requests
def cancelation_handler(bot: Bot, update: Update):

    update.message.reply_text(
        'Введите id сертификата:',
        reply_markup=ReplyKeyboardRemove(),
    )
    return ID

@debug_requests
def id_handler(bot: Bot, update: Update, user_data: dict):
    user_data[ID] = update.message.text
    #logger.info('user_data: %s', user_data)
    maxim = []

    engine = create_engine("postgresql+psycopg2://postgres:12345@127.0.0.1/testbase", echo=True)
    meta = MetaData(engine)

    certificates = Table("certificates", meta, autoload=True)

    conn = engine.connect()
    id = certificates.select()
    ide = conn.execute(id)

    for rew in ide:
        maxim.append(rew[0])
        de = certificates.delete().where(certificates.columns.ident == user_data[ID])
        conn.execute(de)
    update.message.reply_text('Отзываем сертификат')

def datatransfer(name, occupation, maxim):
    validation = "True"
    date = time.strftime("%x", time.localtime())
    filename = ""
    engine = create_engine("postgresql+psycopg2://postgres:12345@127.0.0.1/testbase", echo=True)
    meta = MetaData(engine)

    certificates = Table("certificates", meta, autoload=True)

    conn = engine.connect()
    id1 = certificates.select()
    ide = conn.execute(id1)

    for rew in ide:
        maxim.append(rew[0])
        print(max(maxim))
        filename = "[" + str(max(maxim) + 1) + "]" + ".html"

    users = (name, occupation, date, filename, validation)

    con = psycopg2.connect(
        database="testbase",
        user="postgres",
        password="12345",
        host="127.0.0.1",
        port="5432"
    )
    print("Database opened successfully")
    cur = con.cursor()
    cur.execute(
        f"INSERT INTO certificates (full_name,course_name,date,filename,validation) VALUES {users}"
    )

    con.commit()
    print("Record inserted successfully")
    subprocess.Popen([sys.executable, 'index1.py'])
    con.close()
    print(filename)
    #docu(TG_TOKEN,  filename = "[" + str(max(maxim) + 1) + "]" + ".html")
    return filename

'''def docu(bot: Bot, filename):
    doc = open(filename, 'rb')
    bot.send_document("396358608", doc)'''

@debug_requests
def finish_handler(bot: Bot, update: Update, user_data: dict):
    occupation = update.message.text

    user_data[OCCUPATION] = occupation
    logger.info('user_data: %s', user_data)
    name = user_data[0]
    occupation = user_data[OCCUPATION]


    # Завершить диалог
    update.message.reply_text(f'''
   Все данные успешно сохранены! 
   Вы: {user_data[NAME]}, название курса: {user_data[OCCUPATION]}, 
   сейчас пришлём вам сертификат 
   ''' + "http://127.0.0.1:5000/")

    datatransfer(name, occupation, maxim)

    return ConversationHandler.END, name, occupation


@debug_requests
def cancel_handler(bot: Bot, update: Update):
    """ Отменить весь процесс диалога. Данные будут утеряны
    """

    update.message.reply_text('Отмена. Для начала с нуля нажмите /start')
    return ConversationHandler.END


@debug_requests
def echo_handler(bot: Bot, update: Update):
    update.message.reply_text(
        'Нажмите /start для заполнения анкеты!',
        reply_markup=ReplyKeyboardRemove(),
    )


def main():
    print("start bot")
    logger.info('Start bot')
    bot = Bot(
        token=TG_TOKEN,
    )
    updater = Updater(
        bot=bot,
    )

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start_handler),
            CommandHandler('stop', cancelation_handler)
        ],
        states={
            NAME: [
                MessageHandler(Filters.all, name_handler, pass_user_data=True),
            ],

            OCCUPATION: [
                MessageHandler(Filters.all, finish_handler, pass_user_data=True),
            ],
            ID:[
                MessageHandler(Filters.all, id_handler, pass_user_data=True),
            ]
        },
        fallbacks=[
            CommandHandler('cancel', cancel_handler),
        ],
    )
    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(MessageHandler(Filters.all, echo_handler))

    updater.start_polling()
    updater.idle()
    logger.info('Finish bot')


if __name__ == '__main__':
    main()
