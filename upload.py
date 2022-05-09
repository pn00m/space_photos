import os
import time

import telegram
from dotenv import load_dotenv


def main():
    load_dotenv()
    path = 'images'
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    channel_id = os.environ['TELEGRAM_CHANNEL_ID']
    bot = telegram.Bot(token=bot_token)
    cycle_delay = os.getenv('DELAY', 86400)
    for filenames in os.walk(path):
        for filename in filenames[2]:
            time.sleep(int(cycle_delay))
            with open(path+'/'+filename, 'rb') as space_photo_file:
                bot.send_document(channel_id, space_photo_file)
            os.remove(path+'/'+filename)


if __name__ == '__main__':
    main()
