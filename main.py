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
SUCCESS = 100
FAIL = 300

# Porn download urls of search result
pornList = list()


def search_porn(key_word):
    # The destination website is https://btso.pw

    # Name of an av actress
    # actress = list()

    # Key word of porn, it could be an actress's name, or the porn id, or key words of a porn, etc.
    # keyWord = "FHD"
    # key_word = input("输入关键字")

    page_idx = 1
    num_of_link = 0
    iter_flag = True
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet(key_word + '_search_result')
    url = search + key_word

    http = urllib3.PoolManager()

    while iter_flag:
        if page_idx > 1:
            url = url + "/page_idx/" + str(page_idx)

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
            print('cannot access the website.')
            break

        soup = BeautifulSoup(res.data.decode(), 'html.parser')
        data_list = soup.find('div', attrs={'class': 'data-list'})
        next_page = soup.find('a', attrs={'name': 'nextpage'})

        if data_list:
            print('start to parse the ' + str(page_idx) + 'st page')
            # print(data_list)
            raw_data = data_list.find_all('a')
            # print(raw_data)
            for data in raw_data:
                title = data.get('title')

                link = data.get('href')

                total_info = data.find('div', class_='col-xs-12 size-date visible-xs-block').string.split('/')
                info1 = total_info[0].strip().split(':')
                size = info1[1]

                info2 = total_info[1].strip().split(':')
                date = info2[1]

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
                if av_page.status > 200:
                    print('cannot access the page_idx of this porn.')
                    break

                page_soup = BeautifulSoup(av_page.data.decode(), 'html.parser')
                porn_magnet_link = page_soup.find('textarea', attrs={'class': 'magnet-link'}).string

                worksheet.write(num_of_link, 0, label=title)
                worksheet.write(num_of_link, 1, label=porn_magnet_link)
                worksheet.write(num_of_link, 2, label=size)
                worksheet.write(num_of_link, 3, label=date)
                # worksheet.write(num_of_link, 4, label=porn_magnet_link)
                print(str(num_of_link) + "\t" + title + "\t" + porn_magnet_link + "\t" + size + "\t" + date)
                num_of_link += 1

                time.sleep(2)
            print('finished parsing the ' + str(page_idx) + 'st page.')
        else:
            print('search result handle complete, no more to process.')
            break

        if next_page:
            page_idx += 1
            print('next page is the ' + str(page_idx) + 'st page.')
            time.sleep(2)
        else:
            print('no more pages to process.')
            break

    workbook.save('d:/search_result.xls')


# def parse_porn_magnet_link():


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
