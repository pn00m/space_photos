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
    for root_dir, folders, filenames in os.walk(path):
        for filename in filenames:
            with open(path+'/'+filename, 'rb') as space_photo_file:
                print(space_photo_file)
                bot.send_photo(channel_id, space_photo_file)
                time.sleep(int(cycle_delay))
            os.remove(path+'/'+filename)


if __name__ == '__main__':
    main()
