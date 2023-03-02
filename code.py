import json

import requests

import telegram

from telegram.ext import CommandHandler, Updater

API_KEY = '45fc9fc9cdd6fd6cef98e98872aadf02'

def shorten_url(update, context):

    chat_id = update.message.chat_id

    message_id = update.message.message_id

    url = context.args[0]

    headers = {'Authorization': f'Token {API_KEY}'}

    response = requests.post('https://app.recut.in/api/url/add', json={'url': url}, headers=headers)

    if response.status_code == 200:

        response_json = response.json()

        short_url = response_json['short_url']

        context.bot.send_message(chat_id=chat_id, text=short_url, reply_to_message_id=message_id)

    else:

        response_json = None

        if response.content:

            try:

                response_json = response.json()

            except json.JSONDecodeError:

                pass

        error_message = f"An error occurred while shortening the URL. Status code: {response.status_code}"

        if response_json and response_json.get('detail'):

            error_message += f", detail: {response_json['detail']}"

        context.bot.send_message(chat_id=chat_id, text=error_message)

    if response_json:

        # Format the response as JSON for debugging purposes

        response_json_formatted = json.dumps(response_json, indent=2)

        context.bot.send_message(chat_id=chat_id, text=f"API response:\n{response_json_formatted}")

updater = Updater(token='5975097909:AAFn-28gX-Ftg23BVrybmxuT2fSgGNKN8yo', use_context=True)

dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('shorten', shorten_url))

updater.start_polling()

