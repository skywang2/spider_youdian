import urllib.request
import urllib.parse
import json
import http.cookiejar
import time
import re

# https://ydy1.com/user/login
# https://ydy1.com/page/2


class Pianzi():
    videoname = ''
    video_url = ''
    pic_url = ''

    def __init__(self):
        return


class Youdian():
    page_url = ''           # 主页面url
    login_url = ''
    login_data = {}
    header = {}
    cookie = None
    cookie_handler = None
    http_handler = None
    https_handler = None
    opener = None
    page_num = 0            # 总页数
    pianzi_page_url = []    # 保存片子类
    html = ''               # 页面内容

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
                                         headers=self.header)
        # 使用opener请求管理器发送请求
        response = self.opener.open(request)
        self.html = response.read().decode()
        #p = response.read()
        #p = json.loads(p)
        #print(p['msg'])
        return

    # 获取最后一页页号
    def get_last_page_num(self):
        # 访问第1页
        page_url = self.page_url + str(1)
        response = self.opener.open(page_url)
        self.html = response.read().decode()
        # 解析尾页按钮链接上的页码即可
        tool = Tool()
        self.page_num = tool.get_last_page_num(self.html)

        return

    # 请求第n页
    def get_n_page(self, n):
        page_url = self.page_url + str(n)
        response = self.opener.open(page_url)
        ret = response.read().decode()
        # 解析片子页url
        # 写入文件（或者记录在内存）
        self.html = ret

        return

    # 判断是否正常登录
    def is_login(self):
        tool = Tool()
        if tool.is_login_success(self.html) is True:
            return True
        return False

    def main(self):
        # 请求login
        self.get_login()
        # 获取最后一页页号
        self.get_last_page_num()
        # 请求第n页
        print("login, sleep 2s...")
        time.sleep(2)
        for i in range(self.page_num):
            self.get_n_page(i + 1)
            # 判断第i+1页是否访问成功
            if self.is_login() is False:
                print("page %d is False" %(i + 1))
                self.get_login()
                self.get_n_page(i + 1)
                # 记录失败页号，页号为i，若第一次失败，页号为0，代表一开始的login失败
            path = 'C:\\Users\\skywang\\Desktop\\登录\\' + str(i + 1) + '.html'
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.html)
            print("page %d is True, sleep 2s..." %(i + 1))
            time.sleep(2)
        return


class Tool():
    # 过滤规则
    extract_login = re.compile('<button.*?id="vipLogoutBtn">(.*?)</button>', re.S)
    extract_last_page_num = re.compile('<a href="https://ydy1.com/page/(.*?)".*?class="layui-laypage-last bottom-nav">', re.S)

    def __init__(self):
        return

    # 字符串是否包含中文
    def is_chinese(self, txt):
        for ch in txt:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    # 提取”注销“关键字
    def is_login_success(self, txt):
        ret = re.findall(self.extract_login, txt)
        for t in ret:
            if self.is_chinese(t) is True:
                return True
        return False

    # 提取最后一页页号
    def get_last_page_num(self, txt):
        ret = re.findall(self.extract_last_page_num, txt)
        return int(ret[0])


if __name__ == "__main__":
    page = 'https://ydy1.com/page/'
    login = 'https://ydy1.com/user/login'

    spider = Youdian(page, login)
    # spider.get_login()
    # spider.get_n_page(2)
    # path = 'C:\\Users\\skywang\\Desktop\\登录\\' + str(2) + '.html'
    # with open(path, 'w', encoding='utf-8') as f:
    #     f.write(spider.html)

    spider.main()

    # with open(r'C:\Users\skywang\Desktop\登录\te.html', 'r', encoding='utf-8') as f:
    #     html = f.read()
    #
    # tool = Tool()
    # ret = tool.get_last_page_num(html)
    # ret = int(ret[0])
    # print(ret)
