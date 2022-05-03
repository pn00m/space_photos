import os


import telegram
from dotenv import load_dotenv
import time


def main():
    load_dotenv()
    path = 'images'
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    channel_id = os.environ['TELEGRAM_CHANNEL_ID']
    bot = telegram.Bot(token=bot_token)
    while_condition = True
    try:
        cycle_delay = os.environ['DELAY']
    except KeyError:
        cycle_delay = 86400
    for filenames in os.walk(path):
        for filename in filenames[2]:
            time.sleep(int(cycle_delay))
            bot.send_document(
                            chat_id=channel_id,
                            document=open(path+'/'+filename, 'rb')
                            )
            os.remove(path+'/'+filename)


if __name__ == '__main__':
    main()
