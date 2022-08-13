""" run.py
"""
import logging
import time
import os

import nkparser

from nkcrawler import AzureStorage, DbManipulation


if __name__ == "__main__":
    # Set Database Name
    db_name = "horse_race.db"
    year = os.getenv("YEAR")
    race_id = [os.getenv("RACE_ID")]

    # Load logger config & Set Logger
    logging.basicConfig(level='INFO', format='%(asctime)s [%(levelname)s] %(message)s')
    logger = logging.getLogger()
    # Start logging
    start = time.time()
    logger.info('START nkcrawler')

    # Load Database file from Azure Blob Storage
    az = AzureStorage()
    az.load(db_name)

    # Set Database
    dm = DbManipulation(db_name)

    # Set RACE ID list
    if year is not None:
        race_id = sum([nkparser.race_list(int(year), num) for num in range(1,13)], [])

    # Collect Data    
    for r in race_id:
        for data_type in ["ENTRY", "RESULT", "ODDS"]:
            race = nkparser.load(data_type, r)
            for record in race.table:
                dm.insert_row(data_type, record)
            if data_type == "ENTRY":
                dm.insert_row("RACE", race.info[0])
        dm.commit()

    # Print Log
    elapsed_time = time.time() - start
    logger.info("Finish to load: elapsed time %s sec", elapsed_time)

    az.save(db_name)
