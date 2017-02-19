#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import queue
import time
import requests
import sqlite3

from jdCoupons import Coupon
from jdCoupons import GetCouponsFromHtml
from jdCoupons import GetAllCoupons
from jdBrowser import JdBrowser

db = sqlite3.connect('coupon.db')

def get_list_from_db():
    cur = db.execute('select coupon_id from coupons')
    return [x[0] for x in cur]


if __name__ == '__main__':
    browser = JdBrowser()
    browser.start()
    db.execute('CREATE TABLE IF NOT EXISTS coupons(coupon_id TEXT,climit INTEGER, reduce INTEGER, page INTEGER, item_range TEXT);')

    while True:
        for page, coupon in GetAllCoupons():
            #筛选
            if (coupon.limit - coupon.reduce < 20 or coupon.limit == 0) \
                and coupon.reduce > 30:
                print('Page[{0}] coupon[{1}]'.format(page, coupon))
                if coupon.coupon_id not in get_list_from_db():
                    print('[{0}] auto get'.format(coupon.coupon_id))
                    browser.put_job(page, coupon.coupon_id)
                    db.execute("INSERT INTO coupons VALUES('{0}', {1}, {2}, {3}, \
                        '{4}');".format(coupon.coupon_id, coupon.limit, coupon.reduce, page, coupon.item_range))
                    db.commit()
                else:
                    print('{0} already exist in db'.format(coupon.coupon_id))

        print("sleep 10 minues, start at [{0}]".format(time.asctime()))
        time.sleep(600)
