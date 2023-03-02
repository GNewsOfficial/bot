import requests
import json
import logging
from telegram.ext import Updater, CommandHandler

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define the shorten function
def shorten(update, context):
    # Get the URL to shorten from the command arguments
    args = context.args
    if len(args) == 0:
        update.message.reply_text('Please provide a URL to shorten.')
        return
    url = args[0]

    # Call the Recut API to shorten the URL
    api_key = '45fc9fc9cdd6fd6cef98e98872aadf02'
    api_url = 'https://app.recut.in/api/url/add'
    headers = {'Authorization': f'Bearer {api_key}'}
    data = {'url': url}
    response = requests.post(api_url, headers=headers, data=data)

    # Check the response status code and parse the JSON response
    if response.status_code == 200:
        result = json.loads(response.text)
        shortened_url = result.get('short_url')
        update.message.reply_text(json.dumps({'short_url': shortened_url}))
    else:
        update.message.reply_text(json.dumps({'error': 'Failed to shorten URL.'}))

# Define the main function to start the bot
def main():
    # Set up the Telegram bot and start listening for commands
    updater = Updater(token='5975097909:AAFn-28gX-Ftg23BVrybmxuT2fSgGNKN8yo', use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('shorten', shorten))
    updater.start_polling()

    # Log that the bot has started
    logger.info("Bot started.")

    # Keep the bot running until it is stopped manually
    updater.idle()

if __name__ == '__main__':
    main()
