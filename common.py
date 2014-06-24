#-*-coding:utf8 -*-
import re
import multiprocessing
import pdb
import traceback
import codecs


class FileOper(object):

    '''文件操作类
    文件操作,读取文件,写入文件,根据值写入,根据数组写入等等
    '''

    def file_read(self, file_path):
        '''读取文件内容,返回一个数组
        '''
        result = []
        pc_url = re.compile('^(m|3g)\..*') #m或3g开头直接过滤

        with open(file_path, 'r') as f:
            result = ['http://' + line.replace('\n', '').strip() for line in f.readlines() if not pc_url.search(line)]
        return result

    def file_write(self, file_path, content):
        '''写入内容到某个文件中
        '''
        try:
            # 普通的write和writelines接口无法写入utf8,需要通过codecs的open函数写入
            fw = codecs.open(file_path, 'w', 'utf-8')
            fw.write(content)
            fw.close()
        except:
            print 'error!:'
            print traceback.format_stack()
            fw.close()

    def file_writelines(self, file_path, lines):
        '''写入内容到某个文件中,此时的内容是一个数组
        '''
        try:
            fw = codecs.open(file_path, 'w', 'utf-8')
            fw.writelines([line + '\n' for line in lines])
            fw.close()
        except:
            print 'error!:'
            print traceback.format_stack()
            pdb.set_trace()
            fw.close()


class Config(object):

    '''配置文件类
    存放全局变量
    '''
    url = 'url.txt'         # 存放待采集网站的首页地址
    filter_by_url = 'filter_by_url.txt' #存放经过域名过滤的站点
    filter_by_redirect = 'filter_by_redirect.txt' #存放经过跳转过滤的站点
    filter_by_fingerprint = 'filter_by_fingerprint.txt'
    process_num = 2  # 进程数量,可根据cpu数量选择,一般cpu数量*2即可
    r_fingerprint = re.compile(u'新闻|资讯|门户')
    # 进程间共享数据
    lock = multiprocessing.Lock()  # 进程锁,保证浏览器进程和app进程数量相同
    ipc_list = multiprocessing.Manager().list()  # 存放2级图片链接
    #请求头
    headers = {
        'Connection':'keep-alive',
        'Accept-Language': 'en-US,en;q=0.8',
        'Accept:': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        #'Host': 'www.sina.com.cn',
        'User-Agent':'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D) AppleWebKit/535.19 (KHTML, like     Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19',
        'Accept-Encoding':'gzip,deflate,sdch',
        }
