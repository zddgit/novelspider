import os
import re
import time

import requests
from pyquery import PyQuery

from NovelInfo import Novel23us


# 获取页面
def getHtml(url, encoding, fileName):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = encoding
            return response.text
    except:
        print("网络错误")
        if not os.path.exists(fileName):
            os.mkdir(fileName)
        with open(fileName, "a") as f:
            f.write(url + "\n")
        time.sleep(2)


# 根据页面元素获取具体值
def getContent(html, selector):
    doc = PyQuery(html)
    content = doc(selector)
    return content


# main函数
def main():
    novel_info = Novel23us(1)
    start_url = novel_info.getPageUrl(1)
    html = getHtml(start_url, "utf-8", "pageList.bak")
    content = getContent(html, "#content table tr")
    content.pop(0)
    for item in content:
        novel_url = getContent(item, "a").eq(0).attr.href
        novel_name = getContent(item, "a").eq(0).text()
        print(str(novel_url))
        print(novel_name)
        novel_id = re.search(r'([0-9]+)\.html', str(novel_url)).group(1)
        print(novel_id)


if __name__ == '__main__':
    main()
