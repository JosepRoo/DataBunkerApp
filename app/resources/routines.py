import logging
from flask_restful import Resource

from app.models.uploads.channels.att import ATT
from app.models.uploads.channels.walmart import Walmart


class Routine(Resource):
    channels = {"Walmart": Walmart, "ATT": ATT}

    def post(self, routine: str):
        MAX_RETRIES = 1
        retries = 0
        logging.basicConfig(filename='upload.log', filemode='a', format='%(asctime)s - %(message)s',
                            datefmt='%d-%b-%y %H:%M:%S')
        if routine in Routine.channels:
            channel = Routine.channels.get(routine).build_tree()
        else:
            return "Channel not available: " + routine
        logging.info("********************* Start *********************")
        logging.info(f"Starting {routine}")
        while retries < MAX_RETRIES:
            try:
                res = channel.build_tree()
                logging.info(f"Productos Insertados: {res['inserted']}")
                logging.info(f"Productos Actualizados: {res['updated']}")
                break
            except:
                logging.exception("Exception occurred")
                retries += 1
                if retries == MAX_RETRIES:
                    logging.exception(f"Skipping {routine}")

            retries = 0
            logging.info(f"Ending {routine}")
        logging.info(f"*********************   End   *********************")
        return "Success!! uploaded: " + routine
