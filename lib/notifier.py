import telegram
import traceback
import logging
import random
from lib.sslless_session import SSLlessSession

from telegram.constants import ParseMode

class NullNotifier:
    def notify(self, properties):
        pass

class Notifier(NullNotifier):
    def __init__(self, config, disable_ssl):
        logging.info(f"Setting up bot with token {config['token']}")
        self.config = config
        if disable_ssl:
            self.bot = telegram.Bot(token=self.config['token'], request=SSLlessSession())
        else:
            self.bot = telegram.Bot(token=self.config['token'])
        

    async def notify(self, properties):
        logging.info(f'Notifying about {len(properties)} properties')
        text = random.choice(self.config['messages'])
        try:
            await self.bot.send_message(chat_id=self.config['chat_id'], text=text)
            for prop in properties:
                try:
                    logging.info(f"Notifying about {prop['url']}")
                    message = await self.bot.send_message(chat_id=self.config['chat_id'], 
                            text=f"[{prop['title']}]({prop['url']})",
                            parse_mode=ParseMode.MARKDOWN)
                    if message:
                        prop['notified'] = 1
                except Exception as msgEx:
                    logging.error(f"Notification failed for property: {prop['url']}")
                    logging.error(msgEx)
                                
        except Exception as e:
            logging.error(traceback.format_exc())
            logging.error(f"Notification failed for the following properties:")
            logging.error('\n'.join(str(p['url']) for p in properties))


    def test(self, message):
        self.bot.send_message(chat_id=self.config['chat_id'], text=message)

    @staticmethod
    def get_instance(config, disable_ssl = False):
        if config['enabled']:
            return Notifier(config, disable_ssl)
        else:
            return NullNotifier()