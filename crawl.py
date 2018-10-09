# coding=utf-8

import requests
from bs4 import BeautifulSoup
import csv,time


fileName=time.strftime('%Y-%m-%d %H_%M_%S ',time.localtime(time.time()))+'rent.csv'
csv_file = open(fileName,"w",newline='',encoding='utf-8')
csv_writer = csv.writer(csv_file, delimiter=',')
idSet=set()

url='https://sh.lianjia.com/zufang/pudong/rp2rp3/'
headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

html=requests.get(url=url,headers=headers).content
soup=BeautifulSoup(html,'html.parser')
pageNum=eval(soup.find('div',class_='page-box house-lst-page-box')['page-data'])
pageNum=pageNum['totalPage']


for page in range(pageNum):
    html=requests.get(url='https://sh.lianjia.com/zufang/pudong/pg{}rp2rp3/'.format(page+1),headers=headers).content
    soup=BeautifulSoup(html,'html.parser')
    infos=soup.select('.house-lst')[0].select('li')

    for info in infos:
        dataId=info['data-id']
        if (dataId not in idSet):
            name=info.find('span',class_='region').text.strip()
            zone=info.find('span',class_='zone').text.strip()
            size=info.find('span',class_='meters').text.strip()
            price=info.find('span',class_='num').text.strip()
            csv_writer.writerow([dataId+"\t",name,zone,size,price])
            idSet.add(dataId)
csv_file.close()