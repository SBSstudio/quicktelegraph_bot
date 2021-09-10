#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import logging
import urllib.parse
import json
import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = '1927945502:AAEziSf-GEPro-soLqjy-gaSETnQZeywPlU'
REQUEST_KWARGS = {
    'proxy_url': 'http://127.0.0.1:1087/',
}

API_URL = "https://api.telegra.ph"
# IDEA add photo type
TITLE, CONTENT, PHOTO = range(3)


def create_telegra_accesstoken():
    params = {
        'short_name': 'Sandbox',
        'author_name': 'Anonymous'
    }

    r = requests.get("%s/createAccount?%s" % (API_URL, urllib.parse.urlencode(params)))
    return r.json()['result']['access_token']


def send_to_telegra(title, content):
    access_token = create_telegra_accesstoken()
    params = {
        'access_token': access_token,
        'author_name': 'Telegraph Uploader Bot',
        'title': title,
        'content': '[{"tag":"p","children":[%s]}]' % json.dumps(content, ensure_ascii=False),
        'return_content': 'false'
    }
    r = requests.post('%s/createPage' % API_URL, data=params)
    result = r.json()
    if result['ok']:
        return result['result']['url']


def new(update, context):
    update.message.reply_text("Enter title")
    return TITLE


def title(update, context):
    title = update.message.text
    context.user_data['title'] = title
    update.message.reply_text("Enter Content.")
    return CONTENT


def content(update, context):
    title = context.user_data['title']
    content = update.message.text
    url = send_to_telegra(title, content)
    update.message.reply_text(url)
    update.message.reply_text('Thank You for using me ❤️ \n\nJoin Update Channel:- @SBS_Studio')
    logger.info("Done.")
    return ConversationHandler.END

def staat(qq):
  url = "https://api.telegram.org/bot"+TOKEN+"/sendphoto"
  data = {
    "chat_id": str(qq),
    "photo": "https://telegra.ph/file/3f81561e07a2fcaadbf26.jpg",
    "caption": "Get instant access to Corona in Sri Lanka 📊 .  Automatically retrieve the latest corona information after adding it to the @SLCovid19slbzonebot Group 🦠 . Use /help for more information. @sl_bot_zone ",
    "parse_mode": "HTML",
    "reply_markup": {
        "inline_keyboard": [
            [
                {
                    "text": " 💎 Youtube  ",
                    "url": "https://www.youtube.com/channel/UCvYfJcTr8RY72dIapzMqFQA"
                }, 
                {
                    "text": " 🔔 ",
                    "callback_data": "/help"
                }
            ]
        ]
    }
}
  headers = {'Content-type': 'application/json'}
  r = requests.post(url, callback_data, data=json.dumps(data), headers=headers)

def start(event):
    staat(event.original_update.message.peer_id.user_id)
    raise events.StopPropagation

def cancel(update, context):
    logger.info("canceled the conversation.")
    update.message.reply_text('Bye, canceled the conversation.')

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    logger.info(socket.gethostname())
    if 'qingfengs' in socket.gethostname():
        updater = Updater(TOKEN, use_context=True, request_kwargs=REQUEST_KWARGS)
    else:
        updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('new', new)],

        states={
            TITLE: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, title)],
            CONTENT: [CommandHandler('cancel', cancel), MessageHandler(Filters.text, content)],

            # PHOTO: [MessageHandler(Filters.photo, photo)),
                    # CommandHandler('skip', skip_photo)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
