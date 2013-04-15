#!/usr/bin/env python
#coding:utf-8
#email:natsuki@myclover.org
#script:record.py
from BeautifulSoup import *
import urllib, urllib2, re

base_URL = 'http://cctalkoj.hujiang.com/chat/chatHistory.aspx?page=92&search=&bias=-480&senderid=&receiverid=&RoomId=323833323235&key=780&range=-1&chatId=0'
#base_URL = 'http://cctalkoj.hujiang.com/chat/chatHistory.aspx?page=247&search=&bias=-480&senderid=&receiverid=&RoomId=323833323238&key=1132&range=-%201&chatId=0'


#解析html对象
class Soup():
    def __init__(self, content):
        self.soup = BeautifulSoup(content)
    def get_html_id(self, id_value):
            #id='wrapper'
            return self.soup.find(id=id_value)
    def get_html_tag(self, tag):
        #tag='head'
        return self.soup.find(tag)

#处理URL
def get_page_value():
    return  re.compile(r'page=(?P<value>\d+)&').findall(base_URL)[0]
def get_down_url(url, page):
    '''当前下载的url'''
    #    global base_PACK
    return url + '&page=' + str(page)

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
    return int(get_page_value())

def down_chat():
    save_page('<html>')
    page_end = get_page_end()
    url = base_URL.replace('page='+str(page_end)+'&', '')
    for i in range(1,page_end + 1):
        print '正在保存Page' + str(i) + get_down_url(url, i)
        soup = Soup(down_page(get_down_url(url, i)))
        if i == 1:
            print page_end
            save_page(soup.get_html_tag('head').prettify() + '<body>')
        save_page('<hr/>Page '+str(i)+'<p/>'+soup.get_html_id('wrapper').prettify())
        if i == page_end:
            save_page('</body></html>')
            break

if __name__ == '__main__':
    down_chat()
