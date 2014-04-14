# -*- coding: utf-8 -*-
r"""
    frontdb
    ~~~~~~~

    Utility for front database.

    :copyright: (c) 2013 by Harvey Wang.
"""
import MySQLdb as myDB 
from .pagination import Pagination

HOST = 'localhost'
USER = 'root'
PASSWORD = ''
DBNAME = 'ue'

def connect_db():
    """Returns a new connection to the database."""
    con = None
    try:
    	con = myDB.connect(HOST, USER, PASSWORD, DBNAME)
    except Exception, e:
    	raise e

    return con 

class QueryDB(object):

    _cursor = None
    count = 0
    
    def __init__(self, con, queryStr):

        self.con = con 
        self.queryStr = queryStr

    def _getCursor(self):

        self._cursor = self.con.cursor()
        self._cursor.execute("set names utf8")

    def getone(self):

        self._getCursor()

        self._cursor.execute(self.queryStr)
        self.results = self._cursor.fetchone()
        self.count = 1

        return self.results

    def getall(self):

        self._getCursor()

        self._cursor.execute(self.queryStr)
        self.count = int(self._cursor.rowcount)
        self.results = self._cursor.fetchall()

        return self.results

    def paginate(self, page, per_page=10, error_out=True):
        """Returns `per_page` items from page `page`. By default it will return if no items were found and the page was larger than 1. This behavor can be displayed by setting `error_out` to `False`.

        Returns an :class:`Pagination` object.
        """
        if error_out and page < 1:
            return

        _limit_statement = ""

    def upin(self):

        self._getCursor()
        try:
            self._cursor.execute(self.queryStr)
            self._cursor.commit()
        except:
            self._cursor.rollback()

    def dic(self):

        dct = {}
        for i in range(self.count):
            dct[i] = self.results[i]
        return dct

if __name__ == '__main__':
    db = connect_db()
    cur = db.cursor()
    update = "UPDATE user SET status = 2 WHERE uid = 4273248" 
    try:
        cur.execute(update)
        cur.connection.commit()
    except:
        cur.connection.rollback()


