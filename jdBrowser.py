import threading
import queue
import time
import sqlite3
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

class JdBrowser(threading.Thread):
    def __init__(self, username, password):
        threading.Thread.__init__(self)
        self.queue = queue.Queue()
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1280, 960)
        self.user = username
        self.pwd = password

    def get_list_from_db(self):
        cur = self.db.execute('select coupon_id from coupons')
        return [x[0] for x in cur]

    def insert_into_db(self, coupon_id):
        sql = "INSERT INTO coupons VALUES('{0}');"
        self.db.execute(sql.format(coupon_id))
        self.db.commit()

    def jd_login(self):
        print('开始登陆京东')
        self.driver.get("https://passport.jd.com/new/login.aspx")
        self.driver.find_element_by_link_text('账户登录').click()
        self.driver.find_element_by_id("loginname").send_keys(self.user)
        self.driver.find_element_by_id("nloginpwd").send_keys(self.pwd)
        is_auth_need = True
        try:
            self.driver.find_element_by_id("authcode")
            self.driver.find_element_by_class_name('verify-ycode')
        except NoSuchElementException:
            is_auth_need = False
            print('不需要输入验证码')
        if not is_auth_need:
            self.driver.find_element_by_id("loginsubmit").click()
            time.sleep(3)
        current_url = self.driver.current_url
        print(current_url)
        if current_url != 'https://www.jd.com/':
            self.driver.save_screenshot('login_failure.png')
            return False
        print('登陆京东成功')
        return True

    def get_coupon(self, page, divid):
        try:
            self.driver.get('https://a.jd.com/coupons.html?page={0}'.format(page))
            self.driver.save_screenshot('coupon_page_{0}.png'.format(page))
            coupon = self.driver.find_element_by_id(divid)

            btn = coupon.find_element_by_tag_name('a')
            print('Button Text is [{0}]'.format(btn.text))
            if btn.text.strip()=='今日已领完':
                print('[{0}] 今日已领完'.format(divid))
                return False

            if btn.text.strip() == "立即使用":
                print('[{0}] already got'.format(divid))
                self.insert_into_db(divid)
                return False

            btn.click()
            time.sleep(1)
            self.driver.save_screenshot('{0}.png'.format(divid))
            print('page [{0}] id [{1}] coupon get success'.format(page, divid))
        except Exception as e:
            print(e)
            return False

        return True

    def put_job(self, page, divid):
        self.queue.put((page,divid))

    def stop(self):
        self.queue.put((-1, 'shutdown'))

    def run(self):
        if not self.jd_login():
            print('jd login failure')
            return
        self.db = sqlite3.connect('coupon.db')
        self.db.execute('CREATE TABLE IF NOT EXISTS coupons(coupon_id TEXT);')
        while True:
            (page, divid) = self.queue.get(block=True)
            if page == -1 or divid == 'shutdown':
                print('browser thread exiting')
                break
            print('page [{0}] id[{1}]'.format(page, divid))
            if divid not in self.get_list_from_db():
                self.get_coupon(page, divid)
                time.sleep(3)
            else:
                print('[{0}]已领'.format(divid))

if __name__ == '__main__':
    q = queue.Queue()
    jd = JdBrowser()
    jd.start()
    jd.stop()
    jd.join()
