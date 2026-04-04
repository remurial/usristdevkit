from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
from flask import Flask, request
import asyncio
import os
import threading
import requests

bot_token = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

flask_app = Flask(__name__)

all_services_text = """Доступные услуги:

Юридическая консультация
Адвокат по жилищным спорам
Договоры
Проведение сделок с недвижимостью
Страховые споры
Адвокат по налогам
Споры по договорам ренты
Признание сделок недействительными
Строительный юрист
Защита чести, достоинства и деловой репутации гражданина
Приватизация
"""

help_text = """Команды:
/start - начать работу с ботом
/all_services - показать все услуги
/pay - перейти к оплате услуги
"""
about_text = """<b>Специализация </b>- бизнес-медиация, в т.ч. в спорах:
- между заказчиками и подрядчиками в сфере строительного подряда;
- в сфере инвестиций;
- корпоративных;
- в делах о банкротстве;
- между участниками перевозки грузов наземным, водным, морским и воздушным видами транспорта

</b>Основная профессия, должность</b>: медиатор, юрист, судебный юрист, руководитель юридической фирмы – более 20 лет.

<b>Интересы и увлечения вне профессиональной сферы деятельности</b>: книги, фильмы; яхтинг, дайвинг (море в любом виде!), горные лыжи, велосипед, походы, прогулки в лес, горы"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Все услуги", callback_data='10'),
         InlineKeyboardButton("Оплатить услугу", callback_data='11')]
    ]
    await context.bot.send_message(
        update.effective_chat.id,
        text="Добро пожаловать! Я могу предоставить Вам юридические услуги.\nТелефон: +7 (924) 303-63-73",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def all_services_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(update.effective_chat.id, all_services_text)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(update.effective_chat.id, help_text)

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open('photo.png', 'rb') as file:
        await context.bot.send_photo(update.effective_chat.id, photo=file, caption=about_text, parse_mode=ParseMode.HTML)
    


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k1 = [[InlineKeyboardButton("Перейти к оплате", url='https://www.tinkoff.ru/rm/schenin.aleksey7/dm2yz63658')]]
    query = update.callback_query
    await query.answer()

    if query.data == "1":
        await context.bot.send_message(update.effective_chat.id, "Стоимость услуги: 30 000 руб", reply_markup=InlineKeyboardMarkup(k1))
    elif query.data == "2":
        await context.bot.send_message(update.effective_chat.id, "Стоимость услуги: 70 000 руб", reply_markup=InlineKeyboardMarkup(k1))
    elif query.data == "3":
        await context.bot.send_message(update.effective_chat.id, "Стоимость услуги: 60 000 руб", reply_markup=InlineKeyboardMarkup(k1))
    elif query.data == "4":
        await context.bot.send_message(update.effective_chat.id, "Стоимость услуги: 50 000 руб", reply_markup=InlineKeyboardMarkup(k1))
    elif query.data == "10":
        await context.bot.send_message(update.effective_chat.id, all_services_text)
    elif query.data == "11":
        keyboard = [
            [InlineKeyboardButton("Консультация", callback_data='1'),
             InlineKeyboardButton("Банкротство", callback_data='2')],
            [InlineKeyboardButton("Недвижимость", callback_data='3'),
             InlineKeyboardButton("Представительство в суде", callback_data='4')]
        ]
        await context.bot.send_message(update.effective_chat.id, "Выберите услугу:", reply_markup=InlineKeyboardMarkup(keyboard))

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Консультация", callback_data='1'),
         InlineKeyboardButton("Банкротство", callback_data='2')],
        [InlineKeyboardButton("Недвижимость", callback_data='3'),
             InlineKeyboardButton("Представительство в суде", callback_data='4')]
    ]
    await context.bot.send_message(update.effective_chat.id, "Выберите услугу:", reply_markup=InlineKeyboardMarkup(keyboard))



loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

ptb_app = ApplicationBuilder().token(bot_token).build()
ptb_app.add_handler(CommandHandler('start', start))
ptb_app.add_handler(CommandHandler('all_services', all_services_command))
ptb_app.add_handler(CommandHandler('pay', pay))
ptb_app.add_handler(CallbackQueryHandler(buttons))


loop.run_until_complete(ptb_app.initialize())


@flask_app.route(f"/{bot_token}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), ptb_app.bot)

    loop.run_until_complete(ptb_app.process_update(update))
    return "ok", 200

@flask_app.route("/")
def index():
    return "Bot is running!", 200


def keep_alive():
    while True:
        import time
        time.sleep(14 * 60)
        try:
            requests.get(f"{WEBHOOK_URL}/")
        except:
            pass

threading.Thread(target=keep_alive, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)s
