import logging
from app.common.database import Database
from app.models.uploads.channels.walmart import Walmart
from app.models.uploads.channels.att import ATT

channels = [Walmart, ATT]
MAX_RETRIES = 3
Database.initialize()
retries = 0
logging.basicConfig(filename='upload.log', filemode='a', format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
logging.warning("********************* Start *********************")
for channel in channels:
    logging.warning(f"Starting {channel.__name__}")
    while retries < MAX_RETRIES:
        try:
            res = channel.build_tree()
            logging.warning(f"Productos Insertados: {res['inserted']}")
            logging.warning(f"Productos Actualizados: {res['updated']}")
            break
        except:
            logging.exception("Exception occurred")
            retries += 1
            if retries == MAX_RETRIES:
                logging.exception(f"Skipping {channel.__name__}")

    retries = 0
    logging.warning(f"Ending {channel.__name__}")
logging.warning(f"*********************   End   *********************")
