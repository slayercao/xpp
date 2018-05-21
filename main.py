# encoding:utf-8
"""
This is the main source file of the project.
The purpose of this project is to find and download those good porn.
Author: slayer.
"""

import sys

import certifi
import requests
import urllib3
from bs4 import BeautifulSoup
import xlwt
import time

home = "https://btso.pw/"
tags = home + "tags"
search = home + "search/"


def search_porn(key_word):
    # The destination website is https://btso.pw

    # Name of an av actress
    # actress = list()

    # Porn download urls of search result
    # pornList = list()

    # Key word of porn, it could be an actress's name, or the porn id, or key words of a porn, etc.
    # keyWord = "FHD"
    # key_word = input("输入关键字")

    page = 0
    num_of_link = 0
    iter_flag = True
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet(key_word + '_search_result')
    url = search + key_word

    http = urllib3.PoolManager()

    while iter_flag:
        if page > 0:
            url = url + "/page/" + str(page)

        res = http.request('GET', url,
                           headers={
                               # "Host": "btso.pw",
                               # "Referer": "https://btso.pw/",
                               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                             "Chrome/66.0.3359.139 Safari/537.36 ",
                               # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                               # "Accept-Encoding": "gzip, deflate, br",
                               "Accept-Language": "zh-CN,zh;q=0.9",  # 这个字段很重要，缺少了这个字段会造成403错误
                               # "Cache-Control": "max-age=0",
                               # "Upgrade-Insecure-Requests": "1"
                           })

        if res.status > 200:
            iter_flag = False
            print('cannot access the website.')
            exit(1)
        soup = BeautifulSoup(res.data.decode(), 'html.parser')

        data_list = soup.find('div', attrs={'class': 'data-list'})
        if data_list:

            # print(data_list)
            raw_data = data_list.find_all('a')
            # print(raw_data)
            for data in raw_data:
                title = data.get('title')

                link = data.get('href')

                av_page = http.request('GET', link,
                                       headers={
                                           # "Host": "btso.pw",
                                           # "Referer": "https://btso.pw/",
                                           "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                                         "Chrome/66.0.3359.139 Safari/537.36 ",
                                           # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                                           # "Accept-Encoding": "gzip, deflate, br",
                                           "Accept-Language": "zh-CN,zh;q=0.9",  # 这个字段很重要，缺少了这个字段会造成403错误
                                           # "Cache-Control": "max-age=0",
                                           # "Upgrade-Insecure-Requests": "1"
                                       })

                total_info = data.find('div', class_='col-xs-12 size-date visible-xs-block').string.split('/')
                info1 = total_info[0].strip().split(':')
                size = info1[1]

                info2 = total_info[1].strip().split(':')
                date = info2[1]

                # print(link + "\t" + title + "\t" + size + "\t" + date)
                worksheet.write(num_of_link, 0, label=link)
                worksheet.write(num_of_link, 1, label=size)
                worksheet.write(num_of_link, 2, label=date)
                worksheet.write(num_of_link, 3, label=title)
                num_of_link += 1

            next_page = soup.find('a', attrs={'name': 'nextpage'})
            if next_page:
                page += 1
                time.sleep(5000)
            else:
                iter_flag = False
        else:
            iter_flag = False

    workbook.save('d:/search_result.xls')


# print(pornList)


# http1 = urllib3.PoolManager()
# req1 = http1.request('GET', 'https://www.taobao.com/')
#
# print(req1.status)
# print(req1.data.decode())

# class XPP():
#    def make_request(self):

#    def search_porn(self):

#    def download_porn(self):

if __name__ == "__main__":
    search_porn("FHD")
