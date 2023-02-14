from telegram.ext import *
from telegram import *
import wiki_search
from weather_parser import get_temperature_of_day
from datetime import date, timedelta
from find_car import search_car_by_num

BOT_KEY = '5527604310:AAF9c5E9n5HluiKj6AB2oBR0bYUlA1yytgg'


def start(update, context):
    update.message.reply_text('Привітик)\nЯк твої справи?😉\nЧекаю твої запити)')


def search_car(update, context):
    update.message.reply_text('Без питань😉\nНапиши номер автівки і я скину тобі всю інформацію')


def make_markup():
    today = date.today()
    date_1 = today + timedelta(days=0)
    date_1 = date_1.strftime('%d')
    date_2 = today + timedelta(days=1)
    date_2 = date_2.strftime('%d')
    date_3 = today + timedelta(days=2)
    date_3 = date_3.strftime('%d')
    date_4 = today + timedelta(days=3)
    date_4 = date_4.strftime('%d')
    date_5 = today + timedelta(days=4)
    date_5 = date_5.strftime('%d')
    date_6 = today + timedelta(days=5)
    date_6 = date_6.strftime('%d')
    date_7 = today + timedelta(days=6)
    date_7 = date_7.strftime('%d')

    keyboard = [
        [
            InlineKeyboardButton(date_1, callback_data=date_1),
            InlineKeyboardButton(date_2, callback_data=date_2),
            InlineKeyboardButton(date_3, callback_data=date_3),
            InlineKeyboardButton(date_4, callback_data=date_4),
            InlineKeyboardButton(date_5, callback_data=date_5),
            InlineKeyboardButton(date_6, callback_data=date_6),
            InlineKeyboardButton(date_7, callback_data=date_7)
            ],
        [
            InlineKeyboardButton('exit', callback_data='exit_to_city')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

city_ = 'дніпро'
def button_checking(update, _):
    query = update.callback_query
    info_ = query.data
    query.answer()
    global city_
    if str(info_) == 'kyiv':
        city_ = 'київ'
        query.delete_message(query.message.message_id)
        query.message.reply_text('Без питань🧐\nОбери дату: ', reply_markup=make_markup())
        pass
    elif str(info_) == 'dnipro':
        city_ = 'дніпро'
        query.delete_message(query.message.message_id)
        query.message.reply_text('Без питань🧐\nОбери дату: ', reply_markup=make_markup())
        pass
    elif str(info_) == 'poltava':
        city_ = 'полтава'
        query.delete_message(query.message.message_id)
        query.message.reply_text('Без питань🧐\nОбери дату: ', reply_markup=make_markup())
        pass
    elif str(info_) == 'exit':
        query.delete_message(query.message.message_id)
        query.message.reply_text('Без питань🧐\nОбери дату: ', reply_markup=make_markup())
    elif str(info_) == 'exit_to_city':
        query.delete_message(query.message.message_id)
        query.message.reply_text(f'Добре)🤨\nВибери місто: ', reply_markup=make_markup_city())
    elif str(info_):
        temp, description = get_temperature_of_day(date=str(info_), city=city_)
        min_t = temp['min']
        max_t = temp['max']
        query.delete_message(query.message.message_id)
        query.message.reply_text(f'Ось температура на {str(info_)} число\nmin => {min_t}\nmax => {max_t}\n{description}', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('exit', callback_data='exit')]]))


def make_markup_city():
    today = date.today()
    date_1 = 'kyiv'
    date_2 = 'dnipro'
    date_3 = 'poltava'
    date_4 = today + timedelta(days=3)
    date_4 = date_4.strftime('%d')
    date_5 = today + timedelta(days=4)
    date_5 = date_5.strftime('%d')
    date_6 = today + timedelta(days=5)
    date_6 = date_6.strftime('%d')
    date_7 = today + timedelta(days=6)
    date_7 = date_7.strftime('%d')

    keyboard = [
        [
            InlineKeyboardButton(date_1, callback_data=date_1)
            ],
        [
            InlineKeyboardButton(date_2, callback_data=date_2)
        ],
        [
            InlineKeyboardButton(date_3, callback_data=date_3)
        ]

        ]

    return InlineKeyboardMarkup(keyboard)
def search_info(update, context):
    update.message.reply_text('Добре)😉\nТоді впиши імя відомої людини\n або інший запит: ')

def weather(update, context):
    temp = get_temperature_of_day()
    update.message.reply_text(f'Добре)🤨\nВибери місто: ', reply_markup=make_markup_city())

def mein_communication(inp_text):
    user_message = str(inp_text).lower()
    if user_message in ('hi', 'hello', 'привіт', 'добрий день'):
        return 'Привітик)\nЯк твої справи?😉\nЧекаю твої запити)'
    if user_message in ('слава україні', 'україна переможе'):
        return 'Героям слава'
    elif len(''.join(user_message.split(' '))) >= 8 and search_car_by_num(user_message.upper())[1]:
        return search_car_by_num(user_message.upper())[0]
    elif wiki_search.search_some_info(user_message):
        return wiki_search.search_some_info(user_message)
    else:
        return 'Вибач😞\nЯ не зміг знайти інформації по запиту'



def handler_message(update, context):
    text = str(update.message.text).lower()
    response = mein_communication(text)
    update.message.reply_text(response)


def error(update, context):
    print(f'Update in the {update} caused error {context.error}')



def main():
    updater = Updater(BOT_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('weather', weather))
    dp.add_handler(CommandHandler('searchcar', search_car))
    dp.add_handler(CommandHandler('search_info', search_info))
    dp.add_handler(MessageHandler(Filters.text, handler_message))
    dp.add_handler(CallbackQueryHandler(button_checking))
    dp.add_error_handler(error)

    updater.start_polling()


main()
