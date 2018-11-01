import os
import random
import re
import time

import requests
from pyquery import PyQuery

from DBhelper import DBhelper
from NovelInfo import Novel23us


# 获取页面
def get_html(url, encoding, file_name):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = encoding
            return response.text
    except IOError as e:
        print("网络错误{}".format(e))
        with open(file_name, "a") as f:
            f.write(url + "\n")
            f.close()


# 根据页面元素获取具体值
def get_content(html, selector):
    doc = PyQuery(html)
    content = doc(selector)
    return content


def get_detail(source_id):
    detail_url = novel_info.get_detail_url(source_id)
    html = get_html(detail_url, "utf-8", "detail.bak")
    tag_text = get_content(html, "#content table a").text()
    tag_id = dics.get(tag_text)
    dbhelper.update(" update novel set tagid = %d where sourceId =%d " % tag_id, source_id)
    detail_list_url = get_content(html, "#content .btnlinks a").eq(0).attr.href
    html = get_html(detail_list_url, "utf-8", "detail_list.bak")
    chapter_list = get_content(html, "#a_main .bdsub table td")
    chapter_id = 0
    for item in chapter_list:
        chapter_id = chapter_id + 1
        chapter_url = get_content(item, "a").attr.href
        novel_id = dbhelper.query_one("select id from novel where sourceId = %d" % source_id)[0]
        title = get_content(item, "a").text()
        dbhelper.update("INSERT into chapter (novelId,chapterId,title,source) VALUES (%d,%d,%s,%s)" % novel_id,
                        chapter_id, title, chapter_url)
        chapter_text = get_chapter_text(chapter_url)
        if chapter_text == 0:
            continue
        else:
            # TODO 文章存起来
            pass


def get_chapter_text(chapter_url):
    html = get_html(chapter_url, "utf-8", "chapter.bak")
    if html is None:
        return 0
    else:
        chapter_text = get_content(html, "#contents").text()
        # print(chapter_text)
        return chapter_text


# 小说列表主入口函数
def get_novel_list_main():
    start_url = novel_info.get_page_url(1)
    html = get_html(start_url, "utf-8", "pageList.bak")
    if html is None:
        return
    count = get_content(html, ".pages .pagelink .last").text()
    novel_info.set_page_count(int(count))
    # 循环获取页面
    for page in range(1, int(count) + 1):
        result = get_novel_list(novel_info.get_page_url(page))
        if result == 0:
            continue


# 从具体网址获取小说信息
def get_novel_list(page_url):
    html = get_html(page_url, "utf-8", "pageList.bak")
    if html is None:
        return 0
    content = get_content(html, "#content table tr")
    content.pop(0)
    # 循环获取页面列表
    novels = list()
    for item in content:
        py_item = get_content(item, "a").eq(0)
        novel_url = py_item.attr.href
        novel_name = py_item.text()
        author = get_content(item, "td").eq(2).text()
        novel_id = re.search(r'([0-9]+)\.html', str(novel_url)).group(1)
        novels.append(str((novel_name, author, int(novel_id))))
    sql = "insert into novel (`name`,author,sourceId) values "
    sql = sql + ",".join(novels)
    print(sql)
    dbhelper.update(sql)
    time.sleep(random.randint(2, 4))
    return 1


# 修复pageList.bak记录的网址
def repair_page_list():
    _lines = None
    with open("pageList.bak") as f:
        _lines = f.readlines()
        f.close()
        os.remove("pageList.bak")
    for _url in _lines:
        get_novel_list(_url.strip("\n"))


if __name__ == '__main__':
    # repair_pageList()
    novel_info = Novel23us(1)
    dics = {}
    dbhelper = DBhelper()

    # get_novel_list_main()
    get_chapter_text("https://www.23us.so/files/article/html/2/2521/1247425.html")
