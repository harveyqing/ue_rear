# -*- coding: utf-8 -*-

import re
import urlparse
from flask import g

from ..utils.frontdb import QueryDB
from ..utils.const import month
from .._settings import SITE_URL

def get_numbers(item):


    verify_query = """SELECT u.uid, u.account, b.job, p.ptype, p.sex 
                                FROM user AS u 
                                LEFT OUTER JOIN basicinfo AS b 
                                ON u.uid = b.bsc_id 
                                LEFT OUTER JOIN property AS p 
                                ON u.uid = p.proper_id
                                WHERE u.status = "5" AND u.status <> "1" 
                                ORDER BY u.uid
                             """
    db = g.fdb

    querydb = QueryDB(db, verify_query)
    querydb.getall()
    verifycount = querydb.count   

    if item == 'user_verify':
        return not verifycount == 0 and verifycount or None


def format_datetime(timestramp):
    timestramp = timestramp.strip()

    time_patter = re.compile(r'(\d{4})-(1[0-2]|[1-9]|0[1-9])-([0-2]\d|3[0-1]|[1-9]) ([0-1]\d|2[0-3]|[1-9]):([0-5]\d|[1-9]):([0-5]\d|[1-9])')

    mt = time_patter.match(timestramp).group(1, 2, 3, 4, 5, 6)
    y = mt[0]
    d = mt[2]
    m = month[int(mt[1])]
    h = mt[3]
    mi = mt[4]
    flag = int(h) < 12 and 'AM' or 'PM' 

    return 'Date: %s %s %s/Time: %s:%s %s' % (d, m, y, h, mi, flag)


def cover_url(url):
    url = url.strip()
    url_components = urlparse.urlparse(url)

    url_base = SITE_URL
    cover = urlparse.urljoin(url_base, url_components.path)

    return cover
