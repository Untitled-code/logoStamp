#!../imagesMergeBot/myvenv/bin/python3
# -*- coding: utf-8 -*-

"""
telegram bot for adding logo on photos and videos with register_next_step handler.
"""

import telebot #pip install pyTelegramBotAPI
from pathlib import Path
import datetime
import logging
import imageLogo
import os
logging.basicConfig(filename='addLogo_bot.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

API_TOKEN = os.environ.get('LOGOSTAMP')
print(API_TOKEN)
bot = telebot.TeleBot(API_TOKEN)

user_dict = {}

class User: #get user data
    def __init__(self, name):
        self.name = name #string for the header
        self.name2 = None #string for the main text

print("Listening...")
logging.debug("Listening...")
# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Привіт! Я бот для нанесення лого на фото.
                                 \n Закинь сюди фотки """)

@bot.message_handler(content_types=['photo'])
def photo(message):
    """Prepairing folder"""
    chat_id = message.chat.id
    name = message.text
    user = User(name)
    user_dict[chat_id] = user
    who_sent = msg['from']['first_name']
    """Prepairing directory with chat_id and output file with timestamp"""
    TIMESTAMP = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3] #with miliseconds
    directory = f'dir_{chat_id}_{who_sent}'
    print(f'Directory: {directory}')
    logging.debug(f'Directory: {directory}')
    Path(directory).mkdir(exist_ok=True)  # creating a new directory if not exist
    print(f'Directory is made... {directory}')
    logging.debug(f'Directory is made... {directory}')
    """Downloading photo"""
    print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    logging.debug('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    logging.debug('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    filename = f"{directory}/image_{TIMESTAMP}.jpg"
    with open(filename, 'wb') as new_file:
        new_file.write(downloaded_file)
    print(filename, directory, TIMESTAMP)
    logging.debug(filename, directory, TIMESTAMP)
    imageLogo.main(filename, directory, TIMESTAMP)
    output_file = f'./{directory}/fp_logo{TIMESTAMP}.jpg'
    file = open(output_file, 'rb')
    bot.send_document(chat_id, file)  # sending file to user
    os.remove(filename)
    os.remove(output_file)
    print(f"Files {filename}, {output_file} were removed")
    logging.debug(f"Files {filename}, {output_file} were removed")

    """End of program"""

@bot.message_handler(content_types=['video'])
def video(message):
    """Prepairing folder"""
    chat_id = message.chat.id
    name = message.text
    user = User(name)
    print(User)
    user_dict[chat_id] = user
    who_sent = msg['from']['first_name']
    """Prepairing directory with chat_id and output file with timestamp"""
    TIMESTAMP = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]  # with miliseconds
    directory = f'dir_{chat_id}_{who_sent}'
    print(f'Directory: {directory}')
    logging.debug(f'Directory: {directory}')
    Path(directory).mkdir(exist_ok=True)  # creating a new directory if not exist
    print(f'Directory is made... {directory}')
    logging.debug(f'Directory is made... {directory}')
    """Downloading video"""
    print('message.video =', message.photo)
    fileID = message.video[-1].file_id
    print('fileID =', fileID)
    logging.debug('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    logging.debug('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will happen after delay 2 seconds.
# bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
# bot.load_next_step_handlers()

bot.infinity_polling()
