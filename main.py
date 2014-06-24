#coding:utf8
import requests
import urlparse
from common import *

if __name__ == "__main__":
    file = FileOper()
    filter_by_url = file.file_read(Config.url)
    file.file_writelines(Config.filter_by_url,filter_by_url)
    all_requests = [requests.get(url, headers=Config.headers,allow_redirects=False) for url in filter_by_url ]
    filter_by_redirect = []
    filter_by_redirect_requests = []
    for req in all_requests:
        if req.status_code<300 or req.status_code >302: 
            filter_by_redirect.append(req.url)
            filter_by_redirect_requests.append(req)
        elif urlparse.urlparse(req.headers['location']).hostname.find('www.') > -1:
            filter_by_redirect.append(req.url)
            filter_by_redirect_requests.append(req)
    file.file_writelines(Config.filter_by_redirect,filter_by_redirect)

    filter_by_fingerprint = []
    for req in filter_by_redirect_requests:
        if req.text.find('utf-8') > -1:
            req.encoding = 'utf-8'
        elif req.text.find('gbk') > -1 or req.text.find('gb2312') > -1:
            req.encoding = 'gbk'
        if Config.r_fingerprint.search(req.text):
            filter_by_fingerprint.append(req.url)
    file.file_writelines(Config.filter_by_fingerprint,filter_by_fingerprint)
