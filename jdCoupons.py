#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import time
from bs4 import BeautifulSoup
import re
headers = { "User-Agent":"User-Agent: Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}

class Coupon:
    def __init__(self, html):
        try:
            self.coupon_id = html.attrs['id']
            self.reduce   = int(html.strong.text);
            self.limit = html.span.text.strip();
            self.item_range = html.p.text
            x = re.match("满(.*)元可用", self.limit)
            if x is None:
                self.limit = 0
            else:
                self.limit = int(x.group(1))
        except Exception as e:
            print(html)
            print(e)

    def __str__(self):
        return "[{3}]满{0}减{1} [{2}]".format(self.limit, self.reduce, self.item_range, self.coupon_id)

def GetCouponsFromHtml(html):
    """
    解析网页中得优惠券
    """
    soup = BeautifulSoup(html, "html.parser")
    quans = soup.find_all('div', class_ = 'quan-item')
    coupons = []
    for i in quans:
        coupons.append(Coupon(i))
    return coupons

def GetAllCoupons():
    s = requests.Session()
    url="http://a.jd.com/coupons.html?page={0}"
    for i in range(1, 101):
        try:
            page = s.get(url.format(i), headers = headers);
            couponList = GetCouponsFromHtml(page.text)
            for coupon in couponList:
                yield i, coupon
        except Exception as e:
            print(e)
            break
        time.sleep(1)


if __name__ == '__main__':
    for i in range(1, 101):
        page = requests.get("http://a.jd.com/coupons.html?page={0}".format(i));
        couponList = GetCouponsFromHtml(page.text)
        print("第{0}页".format(i))
        for coupon in couponList:
            print(coupon)
