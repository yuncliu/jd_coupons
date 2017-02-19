import threading
import queue
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class JdBrowser(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = queue.Queue()
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1280, 960)

    def jd_login(self):
        self.driver.get("https://passport.jd.com/new/login.aspx")
        self.driver.find_element_by_link_text('账户登录').click()
        self.driver.find_element_by_id("loginname").send_keys('')
        self.driver.find_element_by_id("nloginpwd").send_keys("")
        is_auth_need = True
        try:
            self.driver.find_element_by_id("authcode")
            self.driver.find_element_by_class_name('verify-ycode')
        except NoSuchElementException:
            is_auth_need = False
            print('not need to input authcode')
        if not is_auth_need:
            self.driver.find_element_by_id("loginsubmit").click()
            time.sleep(3)
        current_url = self.driver.current_url
        print(current_url)
        if current_url != 'https://www.jd.com/':
            self.driver.save_screenshot('login_failure.png')
            return False
        return True

    def get_coupon(self, page, divid):
        try:
            self.driver.get('https://a.jd.com/coupons.html?page={0}'.format(page))
            self.driver.save_screenshot('coupon_page_{0}.png'.format(page))
            coupon = self.driver.find_element_by_id(divid)
            btn = coupon.find_element_by_class_name('get-coupon')
            print(btn)
            btn.click()
            time.sleep(1)
            self.driver.save_screenshot('{0}.png'.format(divid))

            print('page [{0}] id [{1}] coupon get success'.format(page, divid))
            return True
        except Exception as e:
            print(e)
            return False
    def put_job(self, page, divid):
        self.queue.put((page,divid))

    def stop(self):
        self.queue.put((-1, 'shutdown'))

    def run(self):
        if not self.jd_login():
            print('jd login failure')
            return
        while True:
            (page, divid) = self.queue.get(block=True)
            if page == -1 or divid == 'shutdown':
                print('browser thread exiting')
                break
            print('page [{0}] id[{1}]'.format(page, divid))
            self.get_coupon(page, divid)


if __name__ == '__main__':
    q = queue.Queue()
    jd = JdBrowser()
    jd.start()
    jd.stop()
    jd.join()
