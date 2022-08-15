""" run.py
"""
import logging
import time
import os

import nkparser

from nkcrawler import AzureStorage, DbManipulation


def _load_data(race_id):
    for data_type in ["ENTRY", "RESULT", "ODDS"]:
        race = nkparser.load(data_type, race_id)
        for record in race.table:
            dm.insert_row(data_type, record)
            if data_type == "ENTRY":
                dm.insert_row("RACE", race.info[0])
                horse = nkparser.load("HORSE", record["horse_id"])
                dm.insert_row("HORSE", horse.info[0])
                for hist in horse.table:
                    dm.insert_row("HISTORY", hist)

if __name__ == "__main__":
    # Set Database Name
    db_name = "horse_race.sqlite"
    year = os.getenv("YEAR")
    month = os.getenv("MONTH")
    race_id = os.getenv("RACE_ID")

    # Load logger config & Set Logger
    logging.basicConfig(level='INFO', format='%(asctime)s [%(levelname)s] %(message)s')
    logger = logging.getLogger()
    # Start logging
    logger.info('START nkcrawler')

    # Load Database file from Azure Blob Storage
    az = AzureStorage()
    az.load(db_name)

    # Set Database
    dm = DbManipulation(db_name)

    # Collect Data
    if year is not None and month is not None:
        logger.info("=== START YEAR/MONTH MODE: %s/%s ===", year, month)
        start = time.time()
        for race_id in nkparser.race_list(year, month):
            _load_data(race_id)
            dm.commit()
        # Print Log
        elapsed_time = time.time() - start
        logger.info("Finish to %s loads: %s sec", month, elapsed_time)
    elif year is not None and month is None:
        logger.info("=== START YEAR MODE: %s ===", year)
        for month in range(1,13):
            start = time.time()
            for race_id in nkparser.race_list(year, month):
                _load_data(race_id)
            # Print Log
            elapsed_time = time.time() - start
            logger.info("Finish to %s loads: %s sec", month, elapsed_time)
    else:
        logger.info("=== START RACE_ID MODE: %s ===", race_id)
        start = time.time()
        _load_data(race_id)
        # Print Log
        elapsed_time = time.time() - start
        logger.info("Finish to %s loads: %s sec", month, elapsed_time)

    az.save(db_name)
