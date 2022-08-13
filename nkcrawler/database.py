""" database.py
"""
import logging
import sqlite3

import nkparser

logger = logging.getLogger()

class DbManipulation():
    """ Database Tool
    """
    def __init__(self, db_name):
        self.cursor = sqlite3.connect(db_name)
        for table in ["RACE", "ENTRY", "RESULT", "ODDS"]:
            self.cursor.execute(nkparser.create_table_sql(table))

    def insert_row(self, table, rec):
        """ insert row to database
        """
        keys = ','.join(rec.keys())
        qmarks = ','.join(list('?' * len(rec)))
        values = tuple(rec.values())
        self.cursor.execute(f'INSERT OR REPLACE INTO {table} ({keys}) VALUES ({qmarks})', values)

    def commit(self):
        """ commit
        """
        self.cursor.commit()
