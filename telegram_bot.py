import telegram
import logging
import sys
import os
from fs_util import FsUtil
from telegram.ext import Updater
from telegram.ext import CommandHandler

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

class TelegramBot(object):
    SUBSCRIBER_IDS=[]

    def __init__(self, camera):
        self.camera = camera;

    def subscribe(self, bot, update):
        id=update.message.chat_id
        if not id in self.SUBSCRIBER_IDS:
            self.SUBSCRIBER_IDS.append(id)
        print('TelegramBot:subscribe', id)
        print('TelegramBot:subscribtions', self.SUBSCRIBER_IDS)

        self.bot.send_message(chat_id=id, text="Thanks for subscribing :)")

    def take_img(self, bot, update):
        frame = self.camera.get_frame()
        img_path = FsUtil.save_detection_img(frame, FsUtil.IMG_GLOBAL)
        self.notify_image(img_path)

    def notify_image(self, msg):
        for sub_id in self.SUBSCRIBER_IDS:
            try:
                self.bot.send_photo(chat_id=sub_id, photo=open(msg, 'rb'))
            except:
                print('TelegramBot:Error', sys.exc_info()[0])

    def notify_text(self, msg):
        for sub_id in self.SUBSCRIBER_IDS:
            try:
                self.bot.send_message(chat_id=sub_id, text=msg)
            except:
                print('TelegramBot:Error', sys.exc_info()[0])

    def help(self, bot, update):
        cmd_str = "\sub : subscribe to notifications\n"+"\img : take a snapshot\n"+"\h   : list commands"
        self.bot.send_message(chat_id=update.message.chat_id, text=cmd_str)

    def start(self):
        self.sub_handler = CommandHandler('sub', self.subscribe)
        self.img_handler = CommandHandler('img', self.take_img)
        self.help_handler = CommandHandler('h', self.help)

        self.updater = Updater(token=TOKEN)
        self.bot = telegram.Bot(token=TOKEN)

        print('TELEGRAM_BOT:RUNING:', self.bot.get_me())
        self.notify_text('UP & RUNNIN')

        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(self.img_handler)
        self.dispatcher.add_handler(self.sub_handler)
        self.dispatcher.add_handler(self.help_handler)
        self.updater.start_polling()
