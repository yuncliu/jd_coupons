from jdCoupons import Coupon
username=''
password=''

def rule(coupon):
    """
    coupon.limit        满多少
    coupon.reduce       减多少
    coupon.item_range   类品
    """
    if coupon.reduce <= 30:
        return False
    return (coupon.limit - coupon.reduce < 20 or coupon.limit == 0)
