#!/usr/bin/env python
#coding:utf-8
#email:natsuki@myclover.org
#script:record.py
from BeautifulSoup import *
from urlparse import urlparse, urlunparse, parse_qs, ParseResult
import urllib, urllib2

base_URL = 'http://cctalkoj.hujiang.com/chat/chatHistory.aspx?page=108&search=&bias=-480&senderid=&receiverid=&RoomId=323833323235&key=780&range=-1&chatId=0'
#base_URL = 'http://cctalkoj.hujiang.com/chat/chatHistory.aspx?page=203&search=&bias=-480&senderid=&receiverid=&RoomId=323833323238&key=1132&range=-1&chatId=0'
base_PACK = urlparse(base_URL)

#解析html对象
class Soup():
    def __init__(self, content):
        self.soup = BeautifulSoup(content)
    def get_html_id(self, id_value):
        #id='wrapper'
        return self.soup.find(id=id_value)
    def get_html_tag(self, tag):
        #tag='head'
        return self.soup_all(tag)[0]

#处理URL
def urldecode(query):
    return parse_qs(query)
def get_query_value(query, key):
    return query.get(key)
def get_url_query():
    return base_PACK.query
def get_down_url(page):
    '''当前下载的url'''
#    global base_PACK
    new_query = urldecode(get_url_query())
    new_query['page'] = str(page).split()
    new_query = urllib.urlencode(new_query)
    return urlunparse(ParseResult(scheme = base_PACK.scheme,
                           netloc = base_PACK.netloc,
                           path = base_PACK.path,
                           params = base_PACK.params,
                           query = new_query,
                           fragment = base_PACK.fragment))

#下载页面
def down_page(url):
    req = urllib2.urlopen(url)
    content = req.read()
    return content

#保存页面文件
def save_page(connect):
    fb = open('chat_history.html','aw')
    fb.write(connect)
    fb.close()

#针对这个页面
def get_page_end():
    '''获取聊天记录页数'''
    return int(get_query_value(urldecode(get_url_query()),
                               'page')[0])

def down_chat():
    save_page('<html>')
    page_end = get_page_end()
    for i in range(1,page_end + 1):
        soup = Soup(down_page(get_down_url(i)))
        if i == 1:
            save_page(soup.get_html_tag('head') + '<body>')
        save_page(soup.get_html_id('wrapper'))
        if i == page_end:
            save_page('</body></html>')

if __name__ == '__main__':
    down_chat()
