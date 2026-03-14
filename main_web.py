import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes\

BOT_TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"] 

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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Все услуги", callback_data='10'),
         InlineKeyboardButton("Оплатить услугу", callback_data='11')]
    ]
    await context.bot.send_message(
        update.effective_chat.id,
        text="""Добро пожаловать, я могу предоставить Вам юридические услуги на выбор, по выгодной цене!
Телефон для справок: +7 (924) 303-63-73
Доступные команды:""",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def all_services_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(update.effective_chat.id, all_services_text)


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k1 = [[InlineKeyboardButton("Перейти к оплате", url='https://www.tinkoff.ru/rm/schenin.aleksey7/dm2yz63658')]]

    query = update.callback_query
    await query.answer()

    if query.data == "1":
        await context.bot.send_message(update.effective_chat.id, """Стоимость услуги: 30 000 руб
Для пополнения баланса нажмите на кнопку ниже:
""", reply_markup=InlineKeyboardMarkup(k1))

    elif query.data == "2":
        await context.bot.send_message(update.effective_chat.id, """Стоимость услуги: 70 000 руб
Для пополнения баланса нажмите на кнопку ниже:
""", reply_markup=InlineKeyboardMarkup(k1))

    elif query.data == "3":
        await context.bot.send_message(update.effective_chat.id, """Стоимость услуги: 60 000 руб
Для пополнения баланса нажмите на кнопку ниже:
""", reply_markup=InlineKeyboardMarkup(k1))

    elif query.data == "4":
        await context.bot.send_message(update.effective_chat.id, """Стоимость услуги: 50 000 руб
Для пополнения баланса нажмите на кнопку ниже:
""", reply_markup=InlineKeyboardMarkup(k1))

    elif query.data == "10":
        await context.bot.send_message(update.effective_chat.id, all_services_text)

    elif query.data == "11":
        keyboard = [
            [InlineKeyboardButton("Консультация", callback_data='1'),
             InlineKeyboardButton("Банкротство", callback_data='2')],
            [InlineKeyboardButton("Недвижимость", callback_data='3'),
             InlineKeyboardButton("Представительство в суде", callback_data='4')]
        ]
        await context.bot.send_message(
            update.effective_chat.id,
            "Доступные услуги:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Консультация", callback_data='1'),
         InlineKeyboardButton("Банкротство", callback_data='2')],
        [InlineKeyboardButton("Недвижимость", callback_data='3'),
         InlineKeyboardButton("Представительство в суде", callback_data='4')]
    ]
    await context.bot.send_message(
        update.effective_chat.id,
        "Доступные услуги:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('all_services', all_services_command))
    app.add_handler(CommandHandler('pay', pay))
    app.add_handler(CallbackQueryHandler(buttons))

    #app.run_polling()
    port = int(os.environ.get("PORT", 10000))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        secret_token=BOT_TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}",
    )
