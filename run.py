""" run.py
"""
import logging
from nkcrawler import AzureStorage


if __name__ == "__main__":
    # Load logger config & Set Logger
    logging.basicConfig(level='INFO', format='%(asctime)s [%(levelname)s] %(message)s')
    logger = logging.getLogger()

    # Load configuration file from Azure Blob Storage
    az = AzureStorage()
    # az.save('race.db')
    az.load('race.db')
