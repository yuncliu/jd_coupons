#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re

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
        return "满{0}减{1} [{2}][{3}]".format(self.limit, self.reduce, self.item_range, self.coupon_id)

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
    for i in range(1, 101):
        page = requests.get("http://a.jd.com/coupons.html?page={0}".format(i));
        couponList = GetCouponsFromHtml(page.text)
        for coupon in couponList:
            yield i, coupon


if __name__ == '__main__':
    for i in range(1, 101):
        page = requests.get("http://a.jd.com/coupons.html?page={0}".format(i));
        couponList = GetCouponsFromHtml(page.text)
        print("第{0}页".format(i))
        for coupon in couponList:
            print(coupon)
