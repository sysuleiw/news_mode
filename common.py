#-*-coding:utf8 -*-
import re
import multiprocessing
import traceback
import codecs


class FileOper(object):

    '''文件操作类
    文件操作,读取文件,写入文件,根据值写入,根据数组写入等等
    '''

    def file_read(self, file_path):
        '''读取文件内容,通过域名过滤wap版本,返回一个数组
        '''
        result = []
        with open(file_path, 'r') as f:
            result = [line.replace('\n', '').strip() for line in f.readlines()]
        return result

    def file_writelines(self, file_path, lines):
        '''写数组到文件中
        '''
        try:
            fw = codecs.open(file_path, 'w', 'utf-8')
            fw.writelines([line + '\n' for line in lines])
            fw.flush()
            fw.close()
        except:
            print traceback.format_stack()


class Config(object):

    '''配置文件类
    存放全局变量
    '''
    # 待处理的域名列表
    url = 'input/url.txt'
    # 存放经过域名过滤的站点
    filter_by_url = 'output/filter_by_url.txt'
    # 存放经过30x跳转过滤的站点
    filter_by_redirect = 'output/filter_by_redirect.txt'
    # 存放经过keyword过滤的站点
    filter_by_fingerprint = 'output/filter_by_fingerprint.txt'
    # 记录超时站点
    filter_by_timeout = 'output/timeout.txt'
    # 记录错误站点
    filter_by_errors = 'output/errors.txt'
    # 通过关键字过滤资讯站点
    r_fingerprint = re.compile(u'新闻|资讯|门户')
    # 通过关键字过滤资讯站点
    r_forbidden_fingerprint = re.compile(u'论坛|彩票')
    # 需要过滤的网站类型  wap,bbs
    # wap版域名特征:
    #   1 m.开头
    #   2 3g.开头
    #   3 3g.在域名中间
    r_wap_url = re.compile('(^m\..*)|(.*?(3g|bbs)\..*?)')
    # 获取html head内容,用于分析fingerprint
    # 注意如果有很多字符的情况下不建议使用.*,容易误判,建议使用[\s\S]*,例如获取网页head标签内的内容
    r_get_head = re.compile('<head>([\s\S]*?)</head>')
    # 通过js跳转的代码
    r_js_redirect = re.compile('window\.location(\.href)?\s*=')
    # 该时间内无resp则自动放弃
    timeout_limit = 2
    # 进程间共享数据
    process_num = multiprocessing.cpu_count() * 2  # 进程数量
    lock = multiprocessing.Lock()  # 进程锁
    ipc_list_url = multiprocessing.Manager().list()  # 存放通过url过滤的网址
    ipc_list_redirect = multiprocessing.Manager().list()  # 存放通过url过滤的网址
    ipc_list_fingerprint = multiprocessing.Manager().list()  # 存放通过url过滤的网址
    ipc_list_timeout = multiprocessing.Manager().list()  # 存放通过url过滤的网址
    ipc_list_errors = multiprocessing.Manager().list()  # 存放通过url过滤的网址
    # 请求头
    headers = {
        'Connection': 'keep-alive',
        'Accept-Language': 'en-US,en;q=0.8',
        'Accept:': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        # 'Host': 'www.sina.com.cn', # Host字段不可设置,30x跳转域名可能有变
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19',
        'Accept-Encoding': 'gzip,deflate,sdch',
    }
