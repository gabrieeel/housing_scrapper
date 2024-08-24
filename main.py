#!/usr/bin/env python

import logging
import yaml
import asyncio
from lib.notifier import Notifier
from providers.processor import process_properties
from lib.db_functions import update_notified_status

# logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# configuration    
with open("configuration.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

disable_ssl = False
if 'disable_ssl' in cfg:
    disable_ssl = cfg['disable_ssl']

notifier = Notifier.get_instance(cfg['notifier'], disable_ssl)

async def main():
    new_properties = []
    for provider_name, provider_data in cfg['providers'].items():
        try:
            logging.info(f"Processing provider {provider_name}")
            new_properties += process_properties(provider_name, provider_data)
        except Exception as e:
            logging.error(f"Error processing provider {provider_name}.\n{str(e)}")

    if len(new_properties) > 0:
        try:
            await notifier.notify(new_properties)
        except Exception as e:
            logging.error("error general {e}")

        logging.info('notified?')
        logging.info('\n'.join(str(p.get('notified', '0')) for p in new_properties))

        update_notified_status(new_properties)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
