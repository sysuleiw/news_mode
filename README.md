文件说明如下:
============================================

url.txt:董洲提供的原始域名列表

errors.txt:网络问题导致的出错页面

timeout.txt:访问超时页面,这里的超时是指服务器响应超时

filter_by_url.txt:过滤第一步,通过url特征过滤,以"m."开头或者域名中包含"3g."关键字则干掉;

filter_by_redirect.txt:过滤第二步:
	1. 若服务器返回的响应满足30x跳转并且跳转网址不包含"www"则干掉;
	2. 部分网站通过JS实现跳转,可通过分析Javascript代码包含"window.location(.href)="则干掉

filter_by_fingerprint.txt:过滤最后一步:
	1. 找到页面的<head>标签的innerHTML,如果innerHTML包含"新闻/资讯/门户"则取出来
	2. 不能包含"论坛"关键字

