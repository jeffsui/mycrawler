'''
@Author: Linfeng
@Date: 2020-01-04 09:09:28
@LastEditTime : 2020-01-04 11:25:29
@LastEditors  : test
@FilePath: \20200104\qunaer.py
'''
# 去哪儿网 爬虫实战
import requests
from lxml import etree
import datetime
import time

##创建一个爬虫方法
header ={
    'user-agent':"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"
}
def get_page_max(url,header):
    """
    获取分页最大值
    :return:
    """
    response = requests.get(url,header)
    root = etree.HTML(response.content)
    maxpage = root.xpath('//*[@id="pager-container"]/div/a[8]/text()')
    print(maxpage)


def get_content_info(element,start_key,end_key=None,end=1):
    """
    获取指定元素下的文本,并根据条件截取内容
    :param element: 网页元素
    :param start_key: 截取内容前的文本
    :param end_key:  截取内容后的文本
    :param end:   默认值为1,正序查找;如果反序查找设置为-1
    :return: 返回截取内容str类型
    """
    if element:
        if end == 1:
            data = element[0].xpath('string(.)')
            try:

                start = data.find(start_key)
                end = data.find(end_key)
                return data[len(start_key):end]
            except Exception as e:
                return 'no data'
            # if start == -1:
            #     if data.find(u'免费') !=-1:
            #         return u'免费'
            #     else:
            #         return 'no data'
            # else:
            #     end = data.find(end_key)

        if end == -1:
            data = element[0].xpath('string(.)')
            try:
                start = data.rfind(start_key)
                return data[start + len(start_key):]
            except Exception as e:
                return 'no data'
    else:
        return 'no data'

#https://piao.qunar.com/ticket/list.htm?keyword={city}&region=&from=mpl_search_suggest&page={page}
#//*[@id="pager-container"]/div
def crawl(url,city,header):
    page = 1
    total_page = get_page_max(url,header)
    while page<total_page:
        try:
            page = requests.get(f'{url}?keyword={city}&region=&from=mpl_search_suggest&page={page}',header)
            root = etree.HTML(page.content)
            elements = root.xpath('//*[@id="search-list"')
            sightinfo={}
            for element in elments:
                for i in range(1,16):
                    sightinfo['s_name'] = element.xpath(f'./div[{i}]/div/div[2]/h3/a/text()')[0]
                      if element.xpath(f'./div[{i}]/div/div[2]/div/p/span/text()'):
                        sightinfo['s_address'] = element.xpath(f'./div[{i}]/div/div[2]/div/p/span/text()')[0][3:]
                    else:
                        sightinfo['s_address'] = ""
                    sightinfo['s_level'] = element.xpath(f'./div[{i}]/div/div[2]/div/div[1]/div/span[1]/em/span/text()')[0][3:]
                    sightinfo['s_price'] = get_content_info(element.xpath(f'./div[{i}]/div/div[3]'),u'¥',u' 起')
                    sightinfo['s_month_sold'] = get_content_info(element.xpath(f'./div[{i}]/div/div[3]'),u'月销量：',"",-1)
                    sightinfo['s_city'] =  city
                    sightinfo['s_add_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    export_to_csv('data.csv',sightinfo)
                    time.sleep(1)
                    print(sightinfo)
        except Exception as e:
            print(e)
            break    
    page += 1

def export_to_csv(fileName ='',dataDict={}):
    """
    导出csv方法
    :param fileName: 文件名
    :param dataDict: 爬虫爬取的字典类型的数据
    :return: 生成csv文件
    """
    with open(fileName, 'a+',encoding="utf-8") as f:  # Just use 'w' mode in 3.x
        for value in dataDict.values():
            f.write(value+",")
        f.write("\n")
    

if __name__ == "__main__":
    keyword= u"大连"
    url =f"https://piao.qunar.com/ticket/list.htm?keyword={keyword}"
    crawl(url,keyword,header)


