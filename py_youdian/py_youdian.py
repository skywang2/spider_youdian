import urllib.request
import urllib.parse
import json
import http.cookiejar
import time

# https://ydy1.com/user/login
# https://ydy1.com/page/2


class youdian():
    page_url = ''
    login_url = ''
    login_data = {}
    header = {}
    cookie = None
    cookie_handler = None
    http_handler = None
    https_handler = None
    opener = None
    page_num = 0    #总页数

    def __init__(self, page, login):
        self.page_url = page
        self.login_url = login
        self.header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                    'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400 '
        self.header['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        self.header['referer'] = 'https://ydy1.com/'
        self.login_data['vip_username'] = 'skywang2'
        self.login_data['vip_password'] = '88835925'

        # 创建cookiejar实例
        self.cookie = http.cookiejar.CookieJar()
        # 创建cookie管理器
        self.cookie_handler = urllib.request.HTTPCookieProcessor(self.cookie)
        # 创建http请求管理器
        self.http_handler = urllib.request.HTTPHandler()
        # 创建https请求管理器
        self.https_handler = urllib.request.HTTPSHandler()
        # 创建opener请求管理器
        self.opener = urllib.request.build_opener(self.cookie_handler, self.http_handler, self.https_handler)

        return

    # 请求登录页
    def get_login(self):
        # 将data从字典类型转换成http请求中的data格式，并且是bytes类型
        self.login_data = urllib.parse.urlencode(self.login_data).encode('utf-8')
        # 构造请求对象
        request = urllib.request.Request(self.login_url,
                                         data=self.login_data,
                                         method='POST',
                                         headers=self.header
                                         )
        # 使用opener请求管理器发送请求
        response = self.opener.open(request)
        #p = response.read()
        #p = json.loads(p)
        #print(p['msg'])
        return

    # 获取最后一页页号
    def get_last_page_num(self):
        # 访问第1页
        page_url = self.page_url + str(1)
        response = self.opener.open(page_url)
        html = response.read().decode()
        # 解析尾页按钮链接上的页码即可
        self.page_num = 0;
        return

    # 请求第n页
    def get_n_page(self):
        self.get_last_page_num()
        for i in range(self.page_num):
            page_url = self.page_url + str(self.page_num)
            response = self.opener.open(page_url)
            html = response.read().decode()
            # 解析片子页url
            # 写入文件（或者记录在内存）
        time.sleep(1)

        url = 'https://ydy1.com/14212.html'
        response = self.opener.open(url)
        html = response.read().decode()
        #print(html)
        return

    def main(self):

        return


if __name__ == "__main__":
    page = 'https://ydy1.com/page/'
    login = 'https://ydy1.com/user/login'

    spider = youdian(page, login)
    spider.get_login()
    spider.get_n_page()

