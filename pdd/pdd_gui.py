from threading import Thread
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pymysql
import os, re
import json, requests
import tkinter as tk
from antiContent_Js import js
import execjs


def get_anticontent(q):
    ctx = execjs.compile(js)
    anti_content = ctx.call('result', q)
    return anti_content

class App:
    def __init__(self, width=500, height=300):
        self.w = width
        self.h = height
        self.title = '拼多多下单'
        self.root = tk.Tk(className=self.title)
        self.money = ''
        self.money = tk.StringVar()
        self.frame_2 = tk.Frame(self.root)
        self.play = tk.Button(self.frame_2, text='下单', font=('楷体', 12), fg='Red', width=2, height=1,
                              command=self.make_order)
        self.rev = tk.Button(self.frame_2, text='收货', font=('楷体', 12), fg='Blue', width=2, height=1,
                             command=self.receive_order)
        self.label = tk.Label(self.frame_2, text='请输入下单金额:', padx=5, pady=6)
        self.entry = tk.Entry(self.frame_2, textvariable=self.money, highlightcolor='Fuchsia', highlightthickness=1,
                              width=10)
        self.play1 = tk.Button(self.frame_2, text='金额下单', font=('楷体', 12), fg='Purple', width=5, height=1,
                               command=self.make_money_order)
        self.frame_2.pack()
        self.play.grid(row=0, column=2, ipadx=10, ipady=10)
        self.rev.grid(row=0, column=3, ipadx=10, ipady=10)
        self.label.grid(row=1, column=0)
        self.entry.grid(row=1, column=1)
        self.play1.grid(row=1, column=2, ipadx=10, ipady=10)

    def receive_order(self):
        print('收货')
        self.rev.config(state=tk.DISABLED)
        thread_list = []
        sql = 'select * from port_info where PhoNum!="";'
        results = Mysql_db().R(sql)
        i = 0
        for row in results:
            print(row[4][-4:])
            thread = MyThread(port=str(row[4][-4:]), tel=row[4], type='rev')
            thread.start()
            i += 1
            print("开始第" + str(i) + "个线程")
            thread_list.append(thread)
        self.rev.config(state=tk.NORMAL)

    def make_order(self):
        thread_list = []
        sql = 'select * from port_info where PhoNum!="";'
        results = Mysql_db().R(sql)
        i = 0
        for row in results:
            print(row[4][-4:])
            thread = MyThread(port=str(row[4][-4:]), tel=row[4])
            thread.start()
            i += 1
            print("开始第" + str(i) + "个线程")
            thread_list.append(thread)

    def make_money_order(self):
        money = self.money.get()
        print('money', money)
        thread_list = []
        sql = 'select * from port_info where PhoNum!="";'
        results = Mysql_db().R(sql)
        i = 0
        for row in results:
            print(row[4][-4:])
            thread = MyThread(port=str(row[4][-4:]), tel=row[4], money=money)
            thread.start()
            i += 1
            print("开始第" + str(i) + "个线程")
            thread_list.append(thread)

    def loop(self):
        # 自由拖软件大小
        self.root.resizable(True, True)
        self.root.mainloop()


# 收货
# class MyRecived(Thread):
#     def __init__(self, port="9223", money='', tel=None):
#         super().__init__()
#         self.port = port
#         self.tel = tel
#         self.money = money
#         self.open_browser()
#         options = webdriver.ChromeOptions()
#         options.add_experimental_option("debuggerAddress", "127.0.0.1:" + str(self.port))
#         driver = webdriver.Chrome(chrome_options=options)
#         driver.implicitly_wait(20)
#         self.driver = driver
#
#     def run(self):
#         self.receive_order()
#
#     def open_browser(self):
#         main = r'start chrome.exe --remote-debugging-port=' + str(
#             self.port) + r' --user-data-dir="d:\temp\selenum\AutomationProfile' + str(self.port) + r'"'
#         os.system(main)
#
#     def receive_order(self):
#         print('kai')


class MyThread(Thread):
    def __init__(self, port="9223", money='', tel=None, type='buy'):
        super().__init__()
        self.port = port
        self.tel = tel
        self.money = money
        self.open_browser()
        options = webdriver.ChromeOptions()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:" + str(self.port))
        driver = webdriver.Chrome(chrome_options=options)
        driver.implicitly_wait(20)
        self.driver = driver
        self.a = True
        self.num = 0
        self.type = type

    def run(self):
        if self.type == 'buy':
            self.buy_goods()
        elif self.type == 'rev':
            self.receive_order()

    def open_browser(self):
        main = r'start chrome.exe --remote-debugging-port=' + str(
            self.port) + r' --user-data-dir="d:\temp\selenum\AutomationProfile' + str(self.port) + r'"'
        # print('main',main)
        os.system(main)
        print(99)

    # 获取商品列表
    def get_goods_list(self, ):
        goods_list = []
        goods_list = Mydevice().get_pddorder(self.money)
        return goods_list

    # 循环收货
    def receive_order(self):
        self.login_orno()
        AccessToken = self.save_cookies()
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'AccessToken': AccessToken,
            'Connection': 'keep-alive',
            'Content-Length': '124',
            'Content-Type': 'application/json',
            'Host': 'mobile.yangkeduo.com',
            'Origin': 'http//mobile.yangkeduo.com',
            'Referer': 'http//mobile.yangkeduo.com/addresses.html?sku_id=248370662786&group_id=15038829192&goods_id=8874100379&goods_number=1&page_from=0&refer_page_element=single_buy&source_channel=0&refer_page_name=order_checkout&refer_page_id=10004_1564375136007_CgkaWeTIcD&refer_page_sn=10004&sel_address_id=10909746814&allowed_regions=2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11%2C12%2C13%2C14%2C15%2C16%2C17%2C18%2C19%2C20%2C21%2C22%2C23%2C24%2C25%2C26%2C27%2C28%2C29%2C30%2C31%2C32&unreachable_rec=1&cost_template_id=36485038349396&mall_id=656607316&last_payment_type=2',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }
        a = {
            "offset": "",
            "page": 1,
            "pay_channel_list": ["9", "30", "31", "35", "38", "52", "-1"],
            "size": 1,
            "timeout": 1300,
            "type": "unreceived",
        }
        response = requests.post("http://mobile.yangkeduo.com/proxy/api/api/aristotle/order_list",
                                 headers=headers,
                                 json=a)
        # 4. 打印响应内容
        res=response.text
        print('未收货订单',res )
        res_data=json.loads(res)
        all_orders=res_data.get('orders')
        for order in all_orders:
            order_sn=order.get('order_sn')
            anti_content = get_anticontent(headers['Referer'])
            data = {"anti_content": anti_content}
            rev_url='http://mobile.yangkeduo.com/proxy/api/order/'+order_sn+'/received'
            print('rev_url',rev_url)
            r = requests.post(
                rev_url,
                json=data,
                headers=headers)
            print(r.text)

    # 登陆
    def login(self):
        self.driver.get("http://mobile.yangkeduo.com/goods.html?goods_id=24048465357")
        time.sleep(2)
        self.driver.find_element_by_xpath("//div[@class='phone-login']").click()
        print("登陆拼多多")
        print(self.tel)
        while True:
            time.sleep(1)
            print('continue')
            # tel = input("请输入手机号码")
            try:
                # mobile_yesno=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'user-mobile')))
                mobile_yesno = WebDriverWait(self.driver, 10).until(EC.title_contains(u"登录"))
                print('mobile_yesno', mobile_yesno)
                if mobile_yesno:
                    self.driver.find_element_by_id("user-mobile").clear()
                    self.driver.find_element_by_id("user-mobile").send_keys(str(self.tel))
                    element = self.driver.find_element_by_id("code-button").click()
                time.sleep(2)
                if "mobile.yangkeduo.com/psnl_verification.html" in self.driver.current_url:
                    print("触发拼多多反爬虫验证，请手动验证！")
                    continue
                else:
                    break
            except:
                print('反爬虫异常')
        locator = ("class", "content-info-text")
        while True:
            time.sleep(16)
            # db = pymysql.connect("192.168.0.117", "root", "root", "spcard")
            # cursor = db.cursor()
            sql = 'select smsContent from sms_recv where PhoNum="%s" ORDER BY id DESC' % self.tel
            results = Mysql_db().R(sql)
            # print(sql)
            # cursor.execute(sql)
            # results = cursor.fetchall()
            print('results', results, type(results))
            if results:
                content = results[0][0]
                print('内容', content)
                reg = re.compile(r'您的验证码是(.*?)。')
                a = reg.findall(content)
                print(a)
                check_code = a[0]
                self.driver.find_element_by_id("input-code").clear()
                self.driver.find_element_by_id("input-code").send_keys(check_code)
                sql = 'delete from sms_recv where PhoNum=%s' % self.tel
                Mysql_db().D(sql)
                # cursor.execute()
                # db.commit()
                # db.close()
                time.sleep(2)
                self.driver.find_element_by_id("submit-button").click()
                time.sleep(2)
                if "http://mobile.yangkeduo.com/goods.html" in self.driver.current_url:
                    break
                break
            else:
                print('没有收到验证码')

        if self.type == 'buy':
            self.buy_goods()
        elif self.type == 'rev':
            self.receive_order()

    # 添加默认地址
    def save_cookies(self):
        AccessToken = None
        dictCookies = self.driver.get_cookies()
        for i in dictCookies:
            if i.get('name') == 'PDDAccessToken':
                AccessToken = i.get('value')
        return AccessToken if AccessToken else False

    # 添加地址
    def add_address(self, AccessToken):
        print(2)
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'AccessToken': AccessToken,
            'Connection': 'keep-alive',
            'Content-Length': '124',
            'Content-Type': 'application/json',
            # 'Cookie':'api_uid=rBRcYV0nEV3B3Hn0CO1AAg==; __guid=142971561.3214205080169985000.1562841440266.2559; ua=Mozilla%2F5.0%20(Windows%20NT%206.1%3B%20WOW64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F63.0.3239.132%20Safari%2F537.36; _nano_fp=XpdjX5CYXpTYX0XyXT_3QDWELRO1EHvFC9mroxlT; webp=1; msec=1800000; pdd_user_id=2224868807278; pdd_user_uin=X5NJ5NZNGAMKU6JHV4SB7RKVDA_GEXDA; PDDAccessToken=2BLZFBELUXNCP4FXP2F7QLYGR2EOLCHQSGV7YQCV44TAFT35QKVA1026e8c; rec_list_index=rec_list_index_bAmF6V; rec_list_personal=rec_list_personal_1htfu4; JSESSIONID=1873E9D73F28E85C279B285DF189BCCB; rec_list_orders=rec_list_orders_7JFTVM; goods_detail=goods_detail_INESIq; goods_detail_mall=goods_detail_mall_Ljn8WJ; rc-address-goods=rc-address-goods_bkiteb; monitor_count=12',
            'Host': 'mobile.yangkeduo.com',
            'Origin': 'http//mobile.yangkeduo.com',
            'Referer': 'http//mobile.yangkeduo.com/addresses.html?sku_id=248370662786&group_id=15038829192&goods_id=8874100379&goods_number=1&page_from=0&refer_page_element=single_buy&source_channel=0&refer_page_name=order_checkout&refer_page_id=10004_1564375136007_CgkaWeTIcD&refer_page_sn=10004&sel_address_id=10909746814&allowed_regions=2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11%2C12%2C13%2C14%2C15%2C16%2C17%2C18%2C19%2C20%2C21%2C22%2C23%2C24%2C25%2C26%2C27%2C28%2C29%2C30%2C31%2C32&unreachable_rec=1&cost_template_id=36485038349396&mall_id=656607316&last_payment_type=2',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            # 'VerifyAuthToken':'K4SUH-B05YG_Uv-OEug_1w',
        }
        data = [{"name": "汤豫毅", "mobile": "15605743064", "province_id": 2, "city_id": 52, "district_id": 500,
                 "address": "王府井消防大厦A坐1801", "is_default": 0},
                {"name": "秦卓珈", "mobile": "15606915202", "province_id": 27, "city_id": 343, "district_id": 2912,
                 "address": "劝业场街道南京路258号", "is_default": 0},
                {"name": "申莹洋", "mobile": "15602134512", "province_id": 10, "city_id": 138, "district_id": 1078,
                 "address": "北二环东路135号", "is_default": 0},
                {"name": "肖浩平", "mobile": "16512321112", "province_id": 25, "city_id": 321, "district_id": 2713,
                 "address": "马当路388号", "is_default": 0},
                {"name": "张鸣云", "mobile": "15563112211", "province_id": 31, "city_id": 383, "district_id": 3229,
                 "address": "双浦镇袁浦街1号", "is_default": 0},
                {"name": "裴天馨", "mobile": "13546514541", "province_id": 23, "city_id": 300, "district_id": 2473,
                 "address": "机床厂80号院6号楼(享堂路南) ", "is_default": 0},
                {"name": "魏泽华", "mobile": "15321354442", "province_id": 18, "city_id": 244, "district_id": 2060,
                 "address": "滨河街道77号 ", "is_default": 0},
                {"name": "谭宝名", "mobile": "18112354445", "province_id": 15, "city_id": 211, "district_id": 1770,
                 "address": "前进大街1655号 ", "is_default": 0},
                {"name": "谭小名", "mobile": "18631232112", "province_id": 16, "city_id": 220, "district_id": 1835,
                 "address": "虎踞北路15号南京艺术学院 ", "is_default": 0},
                {"name": "单新阳", "mobile": "13541313112", "province_id": 3, "city_id": 36, "district_id": 399,
                 "address": "大观区海口工业园(332省道南)", "is_default": 0},
                {"name": "李岑成", "mobile": "15263123456", "province_id": 17, "city_id": 233, "district_id": 1959,
                 "address": "朝阳洲云锦路雷池街 ", "is_default": 0},
                {"name": "马向煌", "mobile": "15213412122", "province_id": 22, "city_id": 283, "district_id": 2334,
                 "address": "安乐镇无影山北路", "is_default": 0},
                {"name": "赵今", "mobile": "15245312313", "province_id": 23, "city_id": 300, "district_id": 2473,
                 "address": "机床厂80号院6号楼(享堂路南) ", "is_default": 0},
                {"name": "倪可絮", "mobile": "13555523211", "province_id": 18, "city_id": 244, "district_id": 2060,
                 "address": "滨河街道77号 ", "is_default": 0},
                {"name": "吴文真", "mobile": "15622123221", "province_id": 15, "city_id": 211, "district_id": 1770,
                 "address": "前进大街1655号 ", "is_default": 0},
                {"name": "向靖辉", "mobile": "15512313451", "province_id": 16, "city_id": 220, "district_id": 1835,
                 "address": "虎踞北路15号南京艺术学院 ", "is_default": 0},
                {"name": "卢琛平", "mobile": "18213213112", "province_id": 3, "city_id": 36, "district_id": 399,
                 "address": "大观区山口乡联胜村", "is_default": 0},
                {"name": "尤亿", "mobile": "15012312321", "province_id": 17, "city_id": 233, "district_id": 1959,
                 "address": "君领朝阳28栋104号 ", "is_default": 0},
                {"name": "吕武雯", "mobile": "15154134511", "province_id": 22, "city_id": 283, "district_id": 2334,
                 "address": "济南市天桥区黄岗路北段", "is_default": 0},
                {"name": "黄嘉超", "mobile": "15606915202", "province_id": 27, "city_id": 343, "district_id": 2912,
                 "address": "南京路239号瑞竹大厦2号", "is_default": 0},
                {"name": "冉惠弘", "mobile": "18512321312", "province_id": 10, "city_id": 138, "district_id": 1078,
                 "address": "南开二马路9号", "is_default": 0},
                {"name": "张菲丽", "mobile": "15213532131", "province_id": 25, "city_id": 321, "district_id": 2713,
                 "address": "黄浦区淡水路372号", "is_default": 0},
                {"name": "纪冉久", "mobile": "18531321221", "province_id": 31, "city_id": 383, "district_id": 3229,
                 "address": "袁浦街12号", "is_default": 0},
                {"name": "颜子洋", "mobile": "18556214412", "province_id": 23, "city_id": 300, "district_id": 2473,
                 "address": "营西街28号(近小北关社区) ", "is_default": 0}]
        import random
        data1 = random.choice(data)
        print('data1', data1)
        # data = json.dumps(data1)
        response = requests.post("http://mobile.yangkeduo.com/proxy/api/api/origenes/address", headers=headers,
                                 json=data1)
        # 4. 打印响应内容
        print('添加地址', response.text)
        return 1

    # 下单
    def place_order(self, pdd_id):
        # ele = self.driver.find_element_by_class_name('goods-mall-first-line')
        # ActionChains(self.driver).click(ele).perform()
        # time.sleep(1.5)
        # mall_url = self.driver.current_url
        # reg = re.compile(r'mall_id=(.*?)&')
        # mall_list = reg.findall(mall_url)
        # mall_id = mall_list[0]
        # print('mall_id', mall_id)
        # self.driver.back()
        # time.sleep(2)
        # print('后退', self.driver.current_url)
        self.driver.find_element_by_class_name('goods-direct-btn-new').click()
        time.sleep(2)
        url = self.driver.current_url
        if "mobile.yangkeduo.com/login.html" in url:
            self.login()
        self.driver.find_element_by_css_selector("[class='oc-payment-method oc-p-2']").click()
        time.sleep(1)
        # 点击微信支付
        self.driver.find_element_by_class_name('oc-p-2').click()
        # 点击支付宝支付
        # self.driver.find_element_by_class_name('oc-p-1').click()
        time.sleep(1)
        money = self.driver.find_element_by_class_name('oc-final-amount').text
        money = money.replace('￥', '')
        print('money', money)
        # 点击立即支付
        self.driver.find_element_by_class_name('oc-pay-btn  ').click()
        time.sleep(1.5)
        wx_url = self.driver.current_url
        headers = {
            "Host": "wx.tenpay.com",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Referer": "http://mobile.yangkeduo.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }

        res = requests.get(wx_url, headers=headers, verify=False)
        reg = re.compile(r'var url="(.*?)"')
        pay_link = reg.findall(res.text)[0]
        time.sleep(5)
        order_url = self.driver.current_url
        reg = re.compile(r'order_sn=(.*?)&')
        order_sn = reg.findall(order_url)[0]
        data = {
            "money": money,
            "pay_link": pay_link,
            "pinduo": pdd_id,
            "order_sn": order_sn
        }
        Mydevice().send_pddlink(data)
        print('链接添加完毕')
        self.num += 1

    # 是否登录
    def login_orno(self):
        self.driver.get(
            'http://mobile.yangkeduo.com/order_checkout.html?sku_id=302882201602&group_id=18202816192&goods_id=24048465357&goods_number=1&page_from=101&refer_page_element=single_buy&source_channel=0&refer_page_name=goods_detail&refer_page_id=10014_1564392872851_9NFNyClnxM&refer_page_sn=10014&page_id=10004_1564392874587_UJ77RThTUj&last_payment_type=2&is_back=1')
        time.sleep(1)
        AccessToken = self.save_cookies()
        if not AccessToken:
            print('cookies获取失败')
            self.login()

    # 购买商品
    def buy_goods(self):
        try:
            # 处理地址
            if self.a:
                try:
                    self.login_orno()
                    # self.driver.get(
                    #     'http://mobile.yangkeduo.com/order_checkout.html?sku_id=302882201602&group_id=18202816192&goods_id=24048465357&goods_number=1&page_from=101&refer_page_element=single_buy&source_channel=0&refer_page_name=goods_detail&refer_page_id=10014_1564392872851_9NFNyClnxM&refer_page_sn=10014&page_id=10004_1564392874587_UJ77RThTUj&last_payment_type=2&is_back=1')
                    # time.sleep(1)
                    # AccessToken = self.save_cookies()
                    # if not AccessToken:
                    #     print('cookies获取失败')
                    #     self.login()
                    AccessToken = self.save_cookies()
                    print('AccessToken获取成功', AccessToken)
                    self.driver.get(
                        'http://mobile.yangkeduo.com/order_checkout.html?sku_id=302882201602&group_id=18202816192&goods_id=24048465357&goods_number=1&page_from=101&refer_page_element=single_buy&source_channel=0&refer_page_name=goods_detail&refer_page_id=10014_1564392872851_9NFNyClnxM&refer_page_sn=10014&page_id=10004_1564392874587_UJ77RThTUj&last_payment_type=2&is_back=1')
                    time.sleep(1.5)
                    self.driver.find_element_by_class_name('oc-add-address').click()
                    self.add_address(AccessToken)
                    self.a = False
                except:
                    print('地址存在了')
                    self.a = False
                    pass
            # 先处理是否下单
            play_url = 'http://mobile.yangkeduo.com/personal.html'
            self.driver.get(play_url)
            self.driver.refresh()
            time.sleep(1)
            try:
                ele_num = self.driver.find_element_by_class_name('short-number-tag').text  # 'long-number-tag'
                self.num = int(ele_num)
                print('代付款单数', self.num)
            except Exception as e:
                print('代付款单数二次查找')
                try:
                    ele_num = self.driver.find_element_by_class_name('long-number-tag').text  #
                    self.num = int(ele_num)
                    print('代付款单数2', self.num)
                except Exception as e:
                    print('代付款单数查找失败')
                pass
            goods_list = self.get_goods_list()
            print('goods_list', goods_list)
            for i in goods_list:
                link = i.get('link', 0)
                pdd_id = i.get('pinduo', 0)
                print('代付款单数', self.num)
                if self.num <= 5:
                    self.driver.get(link)
                    self.place_order(pdd_id)
                else:
                    print('订单数限制 退出线程')
                    break
            print('下单完毕')
        except:
            print('异常')
            time.sleep(2)
            self.login()


class Mysql_db():
    def __init__(self, ):
        self.db = pymysql.connect("192.168.0.117", "root", "root", "spcard")
        self.cursor = self.db.cursor()

    def R(self, sql):
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        self.db.close()
        return results

    def D(self, sql):
        self.cursor.execute(sql)
        self.db.commit()
        self.db.close()


class Mydevice():
    def __init__(self):
        self.name = 'xiaomi'
        self.pwd = 'xiaomi'
        self.domain = 'http://192.168.0.117:8000'
        self.token = self.get_token()

    # 获取TOKEN
    def get_token(self):
        r = requests.post(self.domain + '/device_login/', json={"username": self.name, "password": self.pwd})
        if r.status_code == 200:
            json_data = r.json()
            json_data.get('token', 0)
            return json_data.get('token', 0)
        else:
            return 'token invalid'

    # 拉取商品链接
    def get_pddorder(self, money=''):
        json_data = self.get_token()
        headers = {
            "Authorization": self.token
        }
        r = requests.get(self.domain + '/device/pddorder/?money=' + str(money), headers=headers)
        if r.status_code == 200:
            return r.json()
        else:
            return []

    # 发送商品链接
    def send_pddlink(self, data):
        headers = {
            "Authorization": self.token
        }
        r = requests.post(self.domain + '/device/pddorder/', headers=headers, json=data)
        if r.status_code == 200:
            return r.json()
        else:
            return -1


if __name__ == '__main__':
    app = App()
    app.loop()
    # num = sys.argv[1]
    # print('sys.argv', type(sys.argv))
    # money = sys.argv[1]
    # print('money', money)
    # thread_list = []
    # sql = 'select * from port_info where PhoNum!="";'
    # results = Mysql_db().R(sql)
    # i = 0
    # for row in results:
    #     print(row[4][-4:])
    #     thread = MyThread(port=str(row[4][-4:]), tel=row[4])
    #     thread.start()
    #     i += 1
    #     print("开始第" + str(i) + "个线程")
    #     thread_list.append(thread)
