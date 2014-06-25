# coding:utf8
import requests
import urlparse
from common import *
import stackless


def get_by_url(file):
    '''根据域名过滤wap站点'''
    result = file.file_read(Config.url)
    filter_by_url = ['http://' + line for line in result
                     if not Config.r_wap_url.search(line)]
    file.file_writelines(Config.filter_by_url, filter_by_url)
    # 职责链调用
    get_by_redirect(filter_by_url)


def get_response(url, all_resp, filter_by_timeout):
    try:
        resp = requests.get(
            url, headers=Config.headers, allow_redirects=False, timeout=Config.timeout_limit)
        all_resp.append(resp)
    except:
        # 超时异常
        filter_by_timeout.append(url)


def get_redirect_request(all_resp, filter_by_redirect, filter_by_redirect_requests):
    try:
        if req.status_code < 300 or req.status_code > 302:
            filter_by_redirect.append(req.url)
            filter_by_redirect_requests.append(req)
        else:
            hostname = urlparse.urlparse(req.headers['location']).hostname
            if hostname and hostname.find('www.') > -1:
                filter_by_redirect.append(req.url)
                filter_by_redirect_requests.append(req)
    except:
        print 'redirect error: ' + req.url + ':' + str(req.status_code)


def get_by_redirect(filter_by_url):
    '''若目标url包含30x跳转,且跳转之后的域名包含www.关键字'''
    filter_by_timeout = []
    all_resp = []
    for url in filter_by_url:
        stackless.tasklet(get_response)(url, all_resp, filter_by_timeout)
    stackless.run()
    file.file_writelines(Config.filter_by_timeout, filter_by_timeout)

    filter_by_redirect = []
    filter_by_redirect_requests = []
    for req in all_resp:
        stackless.tasklet(get_redirect_request)(
            all_resp, filter_by_redirect, filter_by_redirect_requests)
    stackless.run()
    file.file_writelines(Config.filter_by_redirect, filter_by_redirect)
    get_by_fingerprint(filter_by_redirect_requests)


def get_by_fingerprint(filter_by_redirect_requests):
    '''通过页面关键字识别目标站点'''
    filter_by_fingerprint = []
    for req in filter_by_redirect_requests:
        # requests手动指定页面编码
        if req.text.find('utf-8') > -1:
            req.encoding = 'utf-8'
        elif req.text.find('gbk') > -1 or req.text.find('gb2312') > -1:
            req.encoding = 'gbk'
        head = Config.r_get_head.search(req.text)
        if head:
            # 获取网页head innerHTML
            head_cont = head.group(0)
            if Config.r_fingerprint.search(head_cont):
                filter_by_fingerprint.append(req.url)
    file.file_writelines(Config.filter_by_fingerprint, filter_by_fingerprint)

if __name__ == "__main__":
    file = FileOper()
    get_by_url(file)
