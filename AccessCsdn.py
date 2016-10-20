#coding=utf-8
#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
import time
import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup

#访问页面
def accessUrl(url,headers):
    req =  urllib2.Request(url, headers=headers)
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.code
    except urllib2.URLError, e:
        print e.reason
    else:
        html = response.read()
        return html

#访问当前页的所有博客文章并返回当前页码
def accessArticle(data):
    content = BeautifulSoup(data, "lxml")
    #获取文章超链标签及当面页码标签
    page = content.find_all("span", class_="link_title")
    #从标签中获取当前页页码
    pagenumber = content.find_all("div", class_="pagelist")
    page_num = pagenumber[0].strong.string
    article_num = len(page)
    #从标签中获取文章超链
    for i in page[0:article_num]:
        #articleTitle = i.a.string
        articleTitle = i.a.get_text()
        articleTemp = i.a.get("href")
        articleUrl = "http://blog.csdn.net" + i.a.get("href")
        print "access page " + page_num + " title: " + articleTitle
        #访问当前页博文
        accessUrl(articleUrl,headers)
        time.sleep(2)
    return page_num

if __name__ == '__main__':
    url = "http://blog.csdn.net/cartzhang"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36"
    headers = {'User-Agent':user_agent}

    page_num = 0
    while page_num < 6:
        data = accessUrl(url,headers)
        page_num = int(accessArticle(data))
        NextPageUrl = "http://blog.csdn.net/cartzhang/article/list/" + str(int(page_num)+1)
        url = NextPageUrl