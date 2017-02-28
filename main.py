#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import queue
import time
import requests
import config

from jdCoupons import Coupon
from jdCoupons import GetCouponsFromHtml
from jdCoupons import GetAllCoupons
from jdBrowser import JdBrowser

if __name__ == '__main__':
    browser = JdBrowser(config.username, config.password)
    browser.start()

    while True:
        for page, coupon in GetAllCoupons():
            #筛选
            if config.rule(coupon):
                print('Page[{0}] coupon[{1}]'.format(page, coupon))
                print('[{0}] 添加到队列'.format(coupon.coupon_id))
                browser.put_job(page, coupon.coupon_id)

        print("sleep 10 minues, start at [{0}]".format(time.asctime()))
        time.sleep(600)
