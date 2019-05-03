import sys
import re

from NovelSpider import SpiderTools

from NovelSpider.NovelRes import NovelResource


def duyidu_templet_format(target: NovelResource, current_category_key: str):
    return str(target.category_list[current_category_key] + target.category_template)


def duyidu_chapter_url(target: NovelResource, target_url, mulu_url):
    return target.host + target_url


def quanwenyuedu_templet_format(target: NovelResource, current_category_key: str):
    return str(str(target.category_list[current_category_key]).replace(".html", "") + target.category_template)


def quanwenyuedu_chapter_url(target: NovelResource, target_url, mulu_url):
    return str(mulu_url).replace(target.list_url_template, "") + target_url


def quanwenyuedu_get_page_count(target: NovelResource, html):
    page_count_txt = SpiderTools.get_pyquery_content(html, target.select_category_page_count)
    p = re.findall('\\d+', page_count_txt.text())
    return int(p[1])


duyidu = NovelResource(host="du1du.org", home_page="http://du1du.org/shuku.htm",
                       source_id=1, select_category=".container .mb20 li a", encoding="gbk",
                       category_template='{}.htm',
                       select_novel_line="#novel-list li",
                       select_novel_name=".col-xs-3 a",
                       select_novel_author=".col-xs-2",
                       list_url_template="mulu.htm",
                       select_novel_tag=".col-xs-8 .col-xs-4.list-group-item.no-border a",
                       select_novel_introduction="#shot",
                       select_novel_cover=".img-thumbnail",
                       select_chapter="#chapters-list a",
                       select_chapter_content="#txtContent")

duyidu.templet_format = duyidu_templet_format
duyidu.chapter_url = duyidu_chapter_url

quanwenyuedu = NovelResource(host='www.quanwenyuedu.io', home_page="http://www.quanwenyuedu.io/", source_id=2,
                             select_category=".nav a", encoding="utf-8", category_template='-{}.html',
                             select_category_page_count=".box > .list_page >span:eq(1)",
                             select_novel_line='.box .top',
                             select_novel_name='h3 a',
                             select_novel_author='p span',
                             list_url_template='xiaoshuo.html',
                             select_novel_tag=".top p:eq(2) span",
                             select_novel_introduction=".description p",
                             select_novel_cover=".top img",
                             select_chapter="ul.list li a",
                             select_chapter_content="#content > p")

quanwenyuedu.templet_format = quanwenyuedu_templet_format
quanwenyuedu.chapter_url = quanwenyuedu_chapter_url
quanwenyuedu.get_page_count = quanwenyuedu_get_page_count

SpiderTools.addRes(duyidu.source_id, duyidu)
SpiderTools.addRes(quanwenyuedu.source_id, quanwenyuedu)

if __name__ == '__main__':
    # html = SpiderTools.get_html("http://du1du.org/txt-33897/130802985.htm", encoding='gbk')
    # m = SpiderTools.get_pyquery_content(html, "#txtContent")
    # tag = m.remove("script")
    # print(m.text())
    if len(sys.argv) == 3:
        if int(sys.argv[1]) == 1:
            # 启动 du1du.org
            SpiderTools.sourceid = 1
            duyidu.start(int(sys.argv[2]))
        elif int(sys.argv[1]) == 2:
            # 启动 www.quanwenyuedu.io
            SpiderTools.sourceid = 2
            quanwenyuedu.start(int(sys.argv[2]))
        else:
            raise ValueError("参数个数错误！")
