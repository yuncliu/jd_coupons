#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from jdCoupons import Coupon
from jdCoupons import GetCouponsFromHtml
from jdCoupons import GetAllCoupons
import requests
import sqlite3

import os

def test1():
    if os.access('test.html', os.R_OK):
        print('test.html exist')
    else:
        page = requests.get("http://a.jd.com/coupons.html?page={0}".format(1))
        print('get from internet')
        p = open('test.html', 'w+')
        p.write(page.text)
        p.close()
    f = open('test.html', 'r')
    text = f.read()
    f.close()
    couponList = GetCouponsFromHtml(text)
    for coupon in couponList:
        print(coupon)

def test2():
    db = sqlite3.connect('coupon.db')
    db.execute('CREATE TABLE IF NOT EXISTS coupons(coupon_id TEXT,climit INTEGER, reduce INTEGER, page INTEGER, item_range TEXT);')
    """
    for page, c in GetAllCoupons():
        db.execute("INSERT INTO coupons VALUES('{0}', {1}, {2}, {3}, '{4}');".format(c.coupon_id, c.limit, c.reduce, page, c.item_range))

    db.commit()
    """
    cur = db.execute('select coupon_id from coupons')
    for x in cur:
        print(x[0])
    db.close()

if __name__ == '__main__':
    test2()
