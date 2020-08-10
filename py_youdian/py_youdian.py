import urllib.request
import urllib.parse
import urllib.error
import json
import http.cookiejar
import time
import re


class Pianzi():
    name = ''  # 压缩包名字
    pianzi_url = ''  # 下载页面的url
    download_page_url = ''  # 链接页面url
    download_url1 = ''  # 迅雷链接url
    download_url2 = ''
    download_url3 = ''
    icon_url = ''  # 缩略图url

    def __init__(self):
        return


class Youdian():
    page_url = ''  # 主页面url
    login_url = ''
    share_url = ''  # ajax异步获取下载链接
    login_data = {}
    header = {}
    cookie = None
    cookie_handler = None
    http_handler = None
    https_handler = None
    opener = None
    page_num = 0  # 总页数
    pianzi = []  # 保存片子类
    html = ''  # 页面内容
    file1 = ''

    def __init__(self, page, login, share, filename):
        self.page_url = page
        self.login_url = login
        self.share_url = share
        self.file1 = filename
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
        try:
            response = self.opener.open(request)
            self.html = response.read().decode()
        except urllib.error.URLError as e:
            print("login fail!!!")
            print(e.reason)
            self.html = ''

        return

    # 获取最后一页页号
    def get_last_page_num(self):
        # 访问第1页
        page_url = self.page_url + str(1)
        try:
            response = self.opener.open(page_url)
            self.html = response.read().decode()
            # 解析尾页按钮链接上的页码即可
            tool = Tool()
            self.page_num = tool.get_last_page_num(self.html)
        except urllib.error.URLError as e:
            print('get last page num fail!!!')
            print(e.reason)
            self.html = ''
            self.page_num = 1

        return

    # 请求第n页
    def get_n_page(self, n):
        page_url = self.page_url + str(n)
        try:
            response = self.opener.open(page_url)
            self.html = response.read().decode()
        except urllib.error.URLError as e:
            print('get %d page fail!!!' % (n))
            print(e.reason)
            self.html = ''

        return

    # 获取片子类所有属性
    def get_pianzi_url_icon(self):
        tool = Tool()
        ret = tool.get_pianzi_url_icon(self.html)
        for url, icon in ret:
            print('process url:%s' % (url))
            pianzi = Pianzi()
            pianzi.pianzi_url = url
            pianzi.icon_url = icon
            # 返回链接页面特征码
            pianzi.download_page_url = self.get_link_url(url)
            # 判断有无特征码
            if len(pianzi.download_page_url) > 0:
                # 请求getShareUrl页面
                ret = self.get_name_xunlei(pianzi.download_page_url)
                if len(ret) > 0:
                    pianzi.name = ret['info'].split('|||')[0].split('.')[0]
                    pianzi.download_url1 = ret['durl'].split('|||')[0]
                    #pianzi.download_url2 = ret['durl'].split('|||')[1]
                    #pianzi.download_url3 = ret['durl'].split('|||')[2]
                    self.save_link(pianzi, self.file1)
            self.pianzi.append(pianzi)

        return

    # 请求片子页url,获取链接页面url特征码
    def get_link_url(self, url):
        tool = Tool()
        try:
            response = self.opener.open(url)
            ret = response.read().decode()
            ret = tool.get_link_page_url(ret)
        except urllib.error.URLError as e:
            print('get condition code fail!!!')
            print(e.reason)

        return ret

    # 请求share页面,获取name和迅雷链接url
    def get_name_xunlei(self, te):
        data = {'alias': te}
        data = urllib.parse.urlencode(data).encode('utf-8')
        request = urllib.request.Request(self.share_url, data, method='POST')
        try:
            response = self.opener.open(request)
            ret = response.read().decode()
            ret = json.loads(ret)
        except urllib.error.URLError as e:
            print('get shareUrl fail!!!')
            print(e.reason)
            ret = []

        return ret

    # 保存下载链接(可以设计不同保存方式,以便使用)
    def save_link(self, pianzi, file):
        # 保存片子页url和icon
        # path = 'C:\\Users\\skywang\\Desktop\\登录\\download\\' + file
        with open(file, 'a', encoding='utf-8') as f:
            f.write(pianzi.download_url1 + '\n')
            f.flush()

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
        print("login, sleep 0.5s...")
        time.sleep(0.5)
        for i in range(self.page_num):
            self.get_n_page(i + 1)
            # 判断第i+1页是否访问成功
            if self.is_login() is False:
                print("page %d is False" % (i + 1))
                self.get_login()
                self.get_n_page(i + 1)
                # 记录失败页号，页号为i，若第一次失败，页号为0，代表一开始的login失败
            # 保存page页
            # path = 'C:\\Users\\skywang\\Desktop\\登录\\page\\' + str(i + 1) + '.html'
            # with open(path, 'w', encoding='utf-8') as f:
            #     f.write(self.html)
            #     f.flush()

            # 获取片子类所有属性
            self.get_pianzi_url_icon()

            print("page %d is True, sleep 0.5s..." % (i + 1))
            time.sleep(0.5)

        return


class Tool():
    # 过滤规则
    extract_login = re.compile('<button.*?id="vipLogoutBtn">(.*?)</button>', re.S)
    extract_last_page_num = re.compile('<a href="https://ydy1.com/page/(.*?)".*?class="layui-laypage-last bottom-nav">', re.S)
    extract_pianzi_page_url = re.compile('<div class="entry-img"><a href="(.*?)"><img.*?data-original="(.*?)".*?>', re.S)
    extract_download_page_url = re.compile("<p class='vip-content-text'>.*?<a href='https://ydy1.com/s/(.*?)'.*?</a>", re.S)

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
        if len(ret) > 0:
            return int(ret[0])
        return 1

    # 提取片子页url和缩略图url
    def get_pianzi_url_icon(self, txt):
        ret = re.findall(self.extract_pianzi_page_url, txt)
        return ret

    # 提取链接页面url
    def get_link_page_url(self, txt):
        ret = re.findall(self.extract_download_page_url, txt)
        if len(ret) > 0:
            return ret[0]
        return ''


if __name__ == "__main__":
    page = 'https://ydy1.com/page/'                 # page页
    login = 'https://ydy1.com/user/login'           # 登录页，获取cookie
    share = 'https://ydy1.com//user/getShareUrl'    # ajax获取下载地址
    date = time.strftime("%Y%m%d", time.localtime(time.time()))                   # 获取日期
    savePath = 'C:\\Users\\skywang\\Desktop\\登录\\' + 'youdian' + date + '.txt'   # 文件名
    spider = Youdian(page, login, share, savePath)
    # spider.get_login()
    # spider.get_n_page(2)
    # path = 'C:\\Users\\skywang\\Desktop\\登录\\' + str(2) + '.html'
    # with open(path, 'w', encoding='utf-8') as f:
    #     f.write(spider.html)

    spider.main()

    # with open('C:\\Users\\skywang\\Desktop\\登录\\te.html', 'r', encoding='utf-8') as f:
    #     html = f.read()
    #
    # tool = Tool()
    # ret = tool.get_pianzi_url_icon(html)
    # for page, icon in ret:
    #     print(page)
    #     print(icon)

    # with open('C:\\Users\\skywang\\Desktop\\登录\\pianzi\\pianziye.html', 'r', encoding='utf-8') as f:
    #     html = f.read()
    #
    # tool = Tool()
    # ret = tool.get_link_page_url(html)
