from bs4 import BeautifulSoup
import requests
import time
import os
from threading import Thread

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'}
saveDir = 'C:\\贫道报仇从不隔夜\\'
url = 'https://www.biquge345.com/book/146381/#:~:text=%E8%B4%AB%E9%81%93%E6%8A%A5%E4%BB%87%EF%BC%8C%E4%BB%8E%E4%B8%8D%E9%9A%94'  # 《武灵天下》 目录页

# 获得所有主题的URL
def get_topic(url):
    id = 0
    threads = []

    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.content, 'html.parser')
    tag_lis = soup.find('ul', id='chapters-list').find_all('li')

    for tag_li in tag_lis:
        tag_a = tag_li.find('a')

        if tag_a:
            topic_url = tag_a.get('href')  # 获得主题链接
            topic_url = 'https://www.yuyouge.com' + topic_url  # 主题页面 url
            txt = str.replace(tag_li.find('a').get_text(), 'VIP_', '')  # 主题名称
            txt = str.replace(txt, '正文_', '')  # 主题名称
            if txt[0] == '第':
                print(topic_url + ' ' + txt)
                id += 1
                # get_txt(id, topic_url, txt)
                thread = Thread(target=get_txt, args=(id, topic_url, txt))  # 线程调用文本下载函数，下载主题页面中的文本内容
                thread.start()
                threads.append(thread)
    print(id)
    for t in threads:
        t.join()

# 下载链接页面中的文本内容
def get_txt(id, url, txt):
    # print(response.encoding)
    txt = str.replace(txt, '/', ' ')
    txt = str.replace(txt, '\\', ' ')
    txt_file = '%s%04d-%s.txt' % (saveDir, id, txt)
    # 如果目录不存在，就新建目录
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    # 文件不存在就下载，否则跳过
    if not os.path.exists(txt_file):
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.content, 'html.parser')
        tag_txt = soup.find('div', id='txtContent').get_text(separator='\n')
        # i = tag_txt.find('www.qianyege.com')
        # tag_txt = txt + tag_txt[i+16:]
        # print(tag_txt)
        with open(txt_file, mode='w', encoding='utf8') as f:
            size = f.write(tag_txt)
            f.close()
            print("Threads-(%d) : %s(%d Bytes)" % (id, txt_file, size))


if __name__ == '__main__':
    print('===== 主程序开始 =====')
    start = time.perf_counter()
    get_topic(url)
    # get_txt(12,'https://www.yuyouge.com/book/39764/135943672.html', '第2020章 如影随形')
    tt = time.perf_counter() - start
    print('===== 主程序结束，用时 {:.2f}s ====='.format(tt))
