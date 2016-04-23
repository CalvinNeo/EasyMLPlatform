#coding:utf8
import urllib2
import urllib
import string
import json
import sys
import re
import os
from bs4 import BeautifulSoup

'''
    注意检查翻墙软件是不是在全局代理
'''
def getHtml(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')
    page = urllib2.urlopen(req)
    html = page.read()
    return html

def getJSON(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')
    jsondata = urllib2.urlopen(req)
    return json.loads(str(jsondata.read()))

class CSVCrawl:
    def __init__(self, url, hasHead = False, attr_delim = ",", record_delim = "\n", *args, **kwargs):
        self.url = url
        self.hasHead = hasHead
        self.attr_delim = attr_delim
        self.record_delim = record_delim
        if 'code' in kwargs.keys() and kwargs['code'] != None:
            self.code = kwargs['code']
        else:
            self.code = 'utf8'

    def start(self):
        data = getHtml(self.url)
        records = data.split(self.record_delim)
        if self.hasHead:
            self.head = records[0].split(self.attr_delim)
            del records[0]
        else:
            self.head = []
        self.items = []
        for record in records:
            if record == "":
                break
            data_col = record.split(self.attr_delim)
            # (value,column,head)
            if not self.hasHead: # if no head set head as 0,1,2,3,4,5,6...
                self.head = range(len(data_col))
                self.hasHead = True
            # no data mapper here
            self.items.append(data_col)
        return {'head':self.head , 'items':self.items} 

class JSONCrawl:
    def __init__(self, url, head_tag = 'head', data_tag = 'items', *args, **kwargs):
        self.url = url
        self.head_tag = head_tag
        self.data_tag = data_tag
        if 'code' in kwargs.keys() and kwargs['code'] != None:
            self.code = kwargs['code']
        else:
            self.code = 'utf8'

    def start(self):
        j = getJSON(self.url)
        return {'head':[str(x) for x in j[self.head_tag]] , 'items':j[self.data_tag]} 

class Crawl:
    def __init__(self, url, location, search_lmda = None, *args, **kwargs):
        self.url = url
        if type(location).__name__ == 'function':
            self.locate_lmda = location
            self.locate_css = None
        elif type(location).__name__ in ['str','unicode']:
            self.locate_lmda = None
            self.locate_css = location

        self.search_lmda = search_lmda
        if 'code' in kwargs.keys() and kwargs['code'] != None:
            self.code = kwargs['code']
        else:
            self.code = 'utf8'
            
    def start(self):
        html = getHtml(self.url)
        soup = BeautifulSoup(html, "html.parser")
        if self.locate_lmda != None:
            location = self.locate_lmda(soup)
        elif self.locate_css != None:
            location = soup.select(self.locate_css)[0]
        if(type(location).__name__ != 'NoneType'):
            if self.search_lmda == None:# 默认table
                thead = location.find("thead")
                tbody = location.find("tbody")
                if thead==None or tbody==None:
                    return {'head':None , 
                        'items':[[str(td.string.strip().decode(self.code)) for td in tr.findAll("td")] for tr in location.findAll('tr')]}
                else:
                    return {'head':[str(td.string.strip().decode(self.code)) for td in thead.findAll("td")] , 
                        'items':[[str(td.string.strip().decode(self.code)) for td in tr.findAll("td")] for tr in tbody.findAll('tr')]}
            else:
                return self.search_lmda(soup)
                
if __name__ == '__main__':
    # cr = Crawl("http://127.0.0.1:8091/index/1/",lambda soup:soup.find("table"))
    # cr.start()
    print getHtml('http://127.0.0.1:8091')

# def ddu(tmp):
#     return eval(repr(tmp)[1:])

# def analysisDetails(lis):
#     dic = {}
#     for li in lis:
#         liType = li.find('span')['class'][1]
#         if(liType == static.ORGANIZATION):
#             tmp =  li.contents[1]
#             art = tmp.string
#             if(type(art) == type(None)):
#                 tmp = li.contents[3].string
#             dic['organization'] = eval(repr(tmp)[1:])
#         elif(liType == static.LOCATION):
#             tmp =  li.contents[1]
#             dic['location'] = eval(repr(tmp)[1:])
#         elif(liType == static.MAIL):
#             tmp =  li.find('a').string
#             dic['mail'] = eval(repr(tmp)[1:])
#         elif(liType == static.LINK):
#             tmp = li.find('a').string
#             dic['link'] = eval(repr(tmp)[1:])
#         elif(liType == static.CLOCK):
#             tmp =  li.find('time').string
#             dic['clock'] = eval(repr(tmp)[1:])
#     return dic
# def analysiStats(As):
#     dic = {}
#     for a in As:
#         stat,num = ddu(a.span.string), ddu(a.strong.string)
#         dic[stat] = num
#     return dic
# def findNext(lis):
#     sets = []
#     for li in lis:
#         name = li.find('div').find('h3').find('span').find('a')['href'][1:].lower().replace(' ','')
#         # .lower().replace(' ','')
#         # print repr(name)
#         sets.append(name)
#     return sets


# def start(name):
#     url1 = 'https://github.com/{}?tab=repositories'.format(name)
#     url2 = 'https://github.com/{}/followers'.format(name)
#     url3 = 'https://github.com/{}/following'.format(name)
    
#     # get details    
#     html = getHtml(url1)
#     soup = BeautifulSoup(html)
    
#     name = soup.find('span',{'class','vcard-fullname'}).string
#     if(type(name) == type(None)):
#         name = soup.find('span',{'class','vcard-username'}).string
#     print name
#     VcardDetails = {'name':name}
    
#     ul = soup.find('ul',{'class','vcard-details'})
#     lis = ul.findAll('li')
#     VcardDetails.update(analysisDetails(lis))
#     div = soup.find('div',{'class','vcard-stats'})
#     As = div.findAll('a')
#     VcardDetails.update(analysiStats(As))
    
#     info = json.dumps(VcardDetails)
#     save(info,'info2.json','a')
    
#     # get next
#     nexts = set()
#     html = getHtml(url2)
#     soup = BeautifulSoup(html)
#     ol = soup.find('ol')
#     if(type(ol) != type(None)):
#         lis = ol.findAll('li')
#         nexts.update(findNext(lis))
    
#     html = getHtml(url3)
#     soup = BeautifulSoup(html)
#     ol = soup.find('ol')
#     if(type(ol) != type(None)):
#         lis = ol.findAll('li')
#         nexts.update(findNext(lis))

#     return nexts
# if __name__ == '__main__':
#     name = 'KevinSawicki'
#     start(name)