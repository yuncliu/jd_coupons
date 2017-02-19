#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import queue
import time
import requests
import sqlite3
import config

from jdCoupons import Coupon
from jdCoupons import GetCouponsFromHtml
from jdCoupons import GetAllCoupons
from jdBrowser import JdBrowser

db = sqlite3.connect('coupon.db')

def get_list_from_db():
    cur = db.execute('select coupon_id from coupons')
    return [x[0] for x in cur]

def insert_into_db(coupon, page):
    sql = "INSERT INTO coupons VALUES('{0}', {1}, {2}, {3}, '{4}');"
    db.execute(sql.format(coupon.coupon_id,
        coupon.limit,
        coupon.reduce, page,
        coupon.item_range))
    db.commit()


if __name__ == '__main__':
    browser = JdBrowser(config.username, config.password)
    browser.start()
    db.execute('CREATE TABLE IF NOT EXISTS coupons(coupon_id TEXT,climit INTEGER, reduce INTEGER, page INTEGER, item_range TEXT);')

    while True:
        for page, coupon in GetAllCoupons():
            #筛选
            if config.rule(coupon):
                print('Page[{0}] coupon[{1}]'.format(page, coupon))
                if coupon.coupon_id not in get_list_from_db():
                    print('[{0}] auto get'.format(coupon.coupon_id))
                    browser.put_job(page, coupon.coupon_id)
                    insert_into_db(coupon, page)
                else:
                    print('{0} already exist in db'.format(coupon.coupon_id))

        print("sleep 10 minues, start at [{0}]".format(time.asctime()))
        time.sleep(600)
