import telebot
from urllib.request import urlopen
from bs4 import BeautifulSoup
from teplakokkaBot import get_detect, get_settings
from pathlib import Path
import threading

bot = telebot.TeleBot(get_settings.get_token())


# @bot.message_handler(func=lambda message: message.chat.id not in users)
# def some(message):
#     bot.send_message(message.chat.id, 'Не дозволено общаться с незнакомцами')


list_suffix = ['.png', '.jpg', '.jpeg', ]
users = get_settings.get_users()


def get_course():
    # актуальный курс валют по данным ЦБ
    url = urlopen('https://cbr.ru/')
    bs = BeautifulSoup(url, 'lxml')
    baks = bs.find('div', text='USD').find_parent().find_all('div')[2].text
    eur = bs.find('div', text='EUR').find_parent().find_all('div')[2].text
    cours = {'baks': baks, 'eur': eur}
    return cours


def get_psw():
    with open(get_settings.get_dir_pass(), 'r') as f:
        try:
            data = f.read()
        except FileNotFoundError:
            return 'no pass cорян '

    return str(data)


def get_photo():
    print(threading.current_thread().name)
    task1 = threading.Timer(15.0, work)
    task1.start()


def work():
    print(threading.current_thread().name)
    print("work!")
    if get_detect.check_new_image()[1]:
        send_photo(get_detect.check_new_image()[0])
        print("photo sending")
    get_photo()


@bot.message_handler(func=lambda message: message.chat.id not in users)
def msg(message):
    bot.send_message(message.chat.id, ' Не дозволено общаться с незнакомцами')
    print(message.from_user.id)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    data = message.text
    word = str(data).lower()
    print(word)

    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    elif message.text == 'закинь пароль':
        bot.send_message(message.from_user.id, get_psw())
    elif word == 'бакс':
        bot.send_message(message.from_user.id, get_course()['baks'])
    elif 'евро' in word:
        name = message.from_user.first_name
        bot.send_message(message.from_user.id, get_course()['eur'] + name)
    else:
        with open(get_settings.default_photo_path(), 'rb') as photo:
            bot.send_photo(message.from_user.id, photo=photo)


def send_photo(list_found_photo):
    try:
        for i in list_found_photo:
            if Path(i).suffix in list_suffix:
                for user_id in users:
                    bot.send_message(user_id, text='found detect!')
                    bot.send_photo(user_id, photo=open(i, 'rb'))
            else:
                print('не фото!  {} \n'.format(i))

        get_detect.move_image_to_dir(list_found_photo)

    except telebot.apihelper.ApiTelegramException as e:
        print('не фото!  {} \n'.format(e))
        get_detect.move_image_to_dir(list_found_photo)


get_photo()
bot.polling(non_stop=True, interval=0)

