""" run.py
"""
import logging
import time

import nkparser

from nkcrawler import AzureStorage, DbManipulation

if __name__ == "__main__":
    # Load logger config & Set Logger
    logging.basicConfig(level='INFO', format='%(asctime)s [%(levelname)s] %(message)s')
    logger = logging.getLogger()

    # Load Database file from Azure Blob Storage
    az = AzureStorage()
    az.load('horse_race.db')

    dm = DbManipulation()
    # LOAD & INSERT DATA
    logger.info('Start load')
    for race in ["2012060508", "2010040202", "2007060508", "2017070402"]:
        start = time.time()
        for num in range(1,13):
            entry = nkparser.load("ENTRY", f"{race}{num:02}")
            for rec in entry.info:
                dm.insert_row('race', rec)
            for rec in entry.table:
                dm.insert_row('entry', rec)
            result = nkparser.load("RESULT", f"{race}{num:02}")
            for rec in result.table:
                dm.insert_row('result', rec)
            odds = nkparser.load("ODDS", f"{race}{num:02}")
            for rec in odds.table:
                dm.insert_row('odds', rec)

        dm.commit()
        elapsed_time = time.time() - start
        logger.info("Finish to load %s: elapsed time %s sec", race, elapsed_time)

    az.save('horse_race.db')
