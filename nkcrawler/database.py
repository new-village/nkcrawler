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
        for table in ["race", "entry", "result", "odds", "horse", "history"]:
            self.cursor.execute(nkparser.create_table_sql(table))

    def select_min_date(self):
        """ select minimum year/month from race table
        :returns: Description of return value
        :rtype: String or None
        """
        cur = self.cursor.cursor()
        cur.execute('SELECT min(t2.race_date) FROM entry t1 inner join race t2 on (t1.race_id = t2.id)')
        return cur.fetchone()[0]

    def is_not_horse_exist(self, horse_id):
        """ check horse record existing
        :param horse_id: horse ID
        :returns: Description of return value
        :rtype: String or None
        """
        cur = self.cursor.cursor()
        cur.execute("SELECT rowid FROM horse WHERE id = ?", (horse_id,))
        if cur.fetchone() is None:
            # if there is no records, function return True
            return True
        else:
            # if there is some records, function return False
            return False

    def bulk_insert(self, table_name, records):
        """ insert or replace record to database
        :param table_name: string of table name such as race, entry and etc.
        :param records: list of dict type records
        """
        for record in records:
            self.insert_row(table_name, record)

    def insert_row(self, table_name, record):
        """ insert row to database
        """
        keys = ','.join(record.keys())
        qmarks = ','.join(list('?' * len(record)))
        values = tuple(record.values())
        self.cursor.execute(f'INSERT OR REPLACE INTO {table_name} ({keys}) VALUES ({qmarks})', values)

    def commit(self):
        """ commit
        """
        self.cursor.commit()
