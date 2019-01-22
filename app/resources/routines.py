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
            channel = Routine.channels.get(routine)
        else:
            return "Channel not available: " + routine
        logging.info("********************* Start *********************")
        logging.info(f"Starting {routine}")
        try:
            res = channel.build_tree()
            logging.info(f"Productos Insertados: {res['inserted']}")
            logging.info(f"Productos Actualizados: {res['updated']}")
        except:
            logging.exception("Exception occurred")
            retries += 1
            if retries == MAX_RETRIES:
                logging.exception(f"Skipping {routine}")

            logging.info(f"Ending {routine}")
        logging.info(f"*********************   End   *********************")
        return "Success!! uploaded: " + routine
