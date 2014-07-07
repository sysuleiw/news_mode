# coding:utf8
import requests
import urlparse
import time
from common import *
from multiprocessing import Pool


def get_by_url(url):
    '''根据域名过滤wap站点'''
    if not Config.r_wap_url.search(url):
        httpurl = 'http://' + url
        Config.ipc_list_url.append(httpurl)
        get_requests(httpurl)


def get_requests(url):
    '''获取对应url的resp
    '''
    try:
        resp = requests.get(
            url, headers=Config.headers, allow_redirects=False, timeout=Config.timeout_limit)
        if resp.status_code < 300 or resp.status_code > 302:
            Config.ipc_list_redirect.append(resp.url)
            get_by_fingerprint(resp)
        else:
            hostname = urlparse.urlparse(resp.headers['location']).hostname
            if hostname and hostname.find('www.') > -1:
                Config.ipc_list_redirect.append(resp.url)
                get_by_fingerprint(resp)
    except requests.exceptions.Timeout:
        # 超时异常
        # redirect error 部分resp中的location只有path
        # filter_by_timeout.append(url)
        Config.ipc_list_timeout.append(url)
    except:
        # 其他错误
        Config.ipc_list_errors.append(url)


def get_by_fingerprint(resp):
    '''通过页面关键字识别目标站点'''
    # requests手动指定页面编码
    if resp.text.find('utf-8') > -1:
        resp.encoding = 'utf-8'
    elif resp.text.find('gbk') > -1 or resp.text.find('gb2312') > -1:
        resp.encoding = 'gbk'
    head = Config.r_get_head.search(resp.text)
    if head:
        # 获取网页head innerHTML
        head_cont = head.group(0)
        if Config.r_fingerprint.search(head_cont):
            Config.ipc_list_fingerprint.append(resp.url)


if __name__ == "__main__":
    file = FileOper()
    result = file.file_read(Config.url)
    start = time.time()
    # 根据url过滤
    pool = Pool(Config.process_num)
    pool.map(get_by_url, result)
    file.file_writelines(Config.filter_by_url, Config.ipc_list_url)
    file.file_writelines(Config.filter_by_timeout, Config.ipc_list_timeout)
    file.file_writelines(Config.filter_by_errors, Config.ipc_list_errors)
    file.file_writelines(Config.filter_by_redirect, Config.ipc_list_redirect)
    file.file_writelines(
        Config.filter_by_fingerprint, Config.ipc_list_fingerprint)
    print '{0}s'.format(time.time() - start)
