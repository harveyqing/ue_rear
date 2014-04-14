# -*- coding: utf-8 -*-
r"""
    content_wrapper
    ~~~~~~~~~~~~~~~

    data wrapper for content handler

    :copyright: (c) 2014 by Harvey Wang.
"""

from flask import g
from .frontdb import QueryDB, connect_db


def content_count(table="work", condition=""):
    """ specified type of work count.
    :param: `table` specify a table to be operated.
    :param: `type` which type to be counted.
    """
    query = """SELECT wid FROM %s as w %s""" % (str(table), condition)

    querydb = QueryDB(g.fdb, query)
    querydb.getall()

    return querydb.count


def list_works(table="work", condition=""):
    """ list all works currently.
    :param: `table` specify a table to be operated.    
    """
    query = """SELECT w.wid, w.time, w.title, w.cover, u.uid, u.account
               FROM %s as w 
               JOIN user as u 
               ON w.author_id = u.uid %s  
               ORDER BY w.time DESC""" % (str(table), str(condition)) 

    querydb = QueryDB(g.fdb, query)
    querydb.getall()
    works = querydb.results

    return works 


def get_work(id):
    """get contents in the `work` table with specified id.
    :param: `id` work id.
    """
    query = """SELECT w.type, w.title, w.content, w.wdescribe,
                      u.uid, u.account   
               FROM work as w 
               JOIN user as u 
               ON w.author_id = u.uid  
               WHERE w.wid=%s AND w.status=0 AND w.check_status<>0 
               ORDER BY w.time DESC""" % (str(id)) 
 
    querydb = QueryDB(g.fdb, query)
    querydb.getone()
    work = querydb.results

    return work


def check_action(id, action='accept'):
    """accept the specified work while checking."""
    db = connect_db()
    cur = db.cursor()
    
    if action == 'accept':
        status = 0
    elif action == 'violate':
        status = 1
    elif action == 'copyright':
        status = 2
    elif action == 'suspect':
        status = 3
    else:
        status = 4
   
    update = "UPDATE work SET check_status=%d WHERE wid=%s" % (status, str(id)) 
    try:                                                   
        cur.execute(update)
        cur.connection.commit()
    except:
        cur.connection.rollback()
 
