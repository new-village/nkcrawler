""" run.py
"""
import logging
import time
from datetime import datetime as dt, timedelta

import nkparser

from nkcrawler import AzureStorage, DbManipulation


if __name__ == "__main__":
    # Load logger config & Set Logger
    logging.basicConfig(level='INFO', format='%(asctime)s [%(levelname)s] %(message)s')
    logger = logging.getLogger()

    # Load Database file from Azure Blob Storage
    FILE_NAME = "horse_race.sqlite"
    az = AzureStorage()
    az.load(FILE_NAME)
    dm = DbManipulation(FILE_NAME)

    # Create target date
    date = dm.select_min_date()
    date = dt.strptime(date, "%Y-%m-%d") - timedelta(days=30) if date is not None else dt.now()

    # Print Log
    start = time.time()
    logger.info("=== START %s/%s COLLECTION ===", date.year, date.month)

    # Load & insert data
    race_ids = nkparser.race_list(date.year, date.month)
    total = len(race_ids) + 1
    for race_id in race_ids:
        current = race_ids.index(race_id) + 1
        logger.info("=== COLLECT: %s (%s/%s) ===", race_id, current, total)
        # collect odds/result/entry
        for table_name in ["odds", "result", "entry"]:
            nkdata = nkparser.load(table_name, race_id)
            dm.bulk_insert(table_name, nkdata.table)
        dm.bulk_insert("race", nkdata.info)
        # collect horse
        for entry in nkdata.table:
            horse = nkparser.load("horse", entry["horse_id"])
            dm.bulk_insert("horse", horse.info)
            dm.bulk_insert("history", horse.table)
        # collect horse result
        for race in horse.table:
            result = nkparser.load("result", race['race_id'])
            dm.bulk_insert("race", result.info)
            dm.bulk_insert("result", result.table)
        dm.commit()

    # Upload db file
    az.save(FILE_NAME)

    # Print Log
    elapsed = time.time() - start
    logger.info("=== FINISH %s/%s COLLECTION: %s sec ===", date.year, date.month, elapsed)
