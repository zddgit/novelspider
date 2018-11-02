import os
import random
import re
import time
from RedisHelper import RedisHelper
import base64

import requests
from pyquery import PyQuery

from DBhelper import DBhelper
from NovelInfo import Novel23us


# pageList.bak 小说列表页面网址
# detail.bak   小说详情 + 小说源id
# img.bak      小说封面网址 + 小说源id
# detail_list.bak  小说章节目录的网址 + 小说源id
# chapter.bak  小说具体章节页面网址 + 小说源id + 章节id


def save_to_file(file_name, save_text):
    def fn():
        if file_name is not None:
            with open(file_name, "a") as f:
                f.write(save_text + "\n")
                f.close()

    return fn


def get_html(url, fn=None, encoding="utf-8", return_type="text"):
    '''获取页面'''
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = encoding
            if return_type == "text":
                return response.text
            elif return_type == "binary":
                return response.content
            else:
                raise ValueError("return_type only uses `text`, `binary` two options")

    except IOError as e:
        print("网络错误{}".format(e))
        if fn is not None:
            fn()


def get_content(html, selector):
    '''根据页面元素获取具体值'''
    if isinstance(html, PyQuery):
        return html(selector)
    else:
        doc = PyQuery(html)
        return doc(selector)


def get_detail(source_id):
    '''根据数据库小说源id生成小说详情页网址，进而获取小说封面，以及章节信息并保存'''
    detail_url = novel_info.get_detail_url(source_id)
    novel_id = dbhelper.query_one("select id from novel where sourceId = %s" % source_id)[0]
    file_name = "detail.bak"
    fn = save_to_file(file_name=file_name, save_text=detail_url + "," + str(source_id))
    html = get_html(detail_url, fn=fn)

    # 保存封面图像到redis
    cover = get_content(html, "#content img").attr.src
    imgfn = save_to_file(file_name="img.bak", save_text=cover + "," + str(source_id))
    bimg = get_html(cover, return_type="binary", fn=imgfn)
    img = str(base64.b64encode(bimg), encoding="utf-8")
    redis_helper.get_redis().set("image_{}".format(novel_id), img)

    # 更新数据库小说标签和简介
    introduction = get_content(html, "#content dd").eq(3)("p").eq(1).text()
    tag_text = get_content(html, "#content table a").text()
    tag_id = dics.get(tag_text)
    dbhelper.update(" update novel set tagid = %s,introduction = %s where sourceId = %s ",
                    (tag_id, introduction, source_id))

    # 具体章节目录
    detail_list_url = get_content(html, "#content .btnlinks a").eq(0).attr.href
    detail_list_fn = save_to_file(file_name="detail_list.bak", save_text=detail_list_url)
    html = get_html(detail_list_url, fn=detail_list_fn)
    chapter_list = get_content(html, "#a_main .bdsub table td")
    chapter_id = 0

    # 循环获取单章
    for item in chapter_list:
        # 保存单章信息来源到数据库
        chapter_id = chapter_id + 1
        chapter_url = get_content(item, "a").attr.href
        title = get_content(item, "a").text()
        sql = "INSERT into chapter (novelId,chapterId,title,source) VALUES (%s,%s,%s,%s)"
        dbhelper.update(sql, (novel_id, chapter_id, title, chapter_url))
        chapter_text = get_chapter_text(chapter_url, source_id, chapter_id)
        if chapter_text == 0:
            continue
        else:
            # 保存单章信息到redis
            redis_helper.get_redis().hset("contents_{}".format(novel_id), chapter_id, chapter_text)
        time.sleep(random.randint(1, 3))


def get_chapter_text(chapter_url, source_id, chapter_id):
    ''' 根据章节url获取内容 '''
    chapter_fn = save_to_file(file_name="chapter.bak",
                              save_text=chapter_url + "," + str(source_id) + "," + str(chapter_id))
    html = get_html(chapter_url, fn=chapter_fn)
    if html is None:
        return 0
    else:
        chapter_text = get_content(html, "#contents").text()
        chapter_text = chapter_text.replace("\n", "")
        return chapter_text


def get_novel_list_main():
    ''' 小说列表主入口函数 '''
    start_url = novel_info.get_page_url(1)
    html = get_html(start_url, fn=save_to_file("pageList.bak", start_url))
    if html is None:
        return
    count = get_content(html, ".pages .pagelink .last").text()
    novel_info.set_page_count(int(count))
    # 循环获取页面
    for page in range(1, int(count) + 1):
        result = get_novel_list(novel_info.get_page_url(page))
        if result == 0:
            continue


def get_novel_list(page_url):
    ''' 从具体网址获取小说列表信息,并保存数据库 '''
    html = get_html(page_url, fn=save_to_file("pageList.bak", page_url))
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


def repair_page_list():
    '''修复小说列表页面失败而记录的网址'''
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
    dbhelper = DBhelper()
    dics = {}
    redis_helper = RedisHelper()
    # dict_list = dbhelper.query("SELECT id,`name` from dictionary where type = 'tag'")
    # for _item in dict_list:
    #     dics[_item[1]] = _item[0]

    # get_novel_list_main()
    get_detail(14239)
