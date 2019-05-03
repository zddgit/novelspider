import random
import time
import zlib

from pyquery import PyQuery

from NovelSpider import SpiderTools
from NovelSpider.DBhelper import DBhelper


class NovelResource:

    def __init__(self, host: str, home_page: str, select_category: str,
                 source_id: int,
                 select_novel_line: str = None,
                 select_novel_name: str = None,
                 select_novel_author: str = None,
                 select_novel_tag: str = None,
                 select_novel_introduction: str = None,
                 select_novel_cover: str = None,
                 select_chapter: str = None,
                 select_chapter_content: str = None,
                 list_url_template: str = None,
                 category_template: str = None,
                 select_category_page_count: str = None,
                 encoding: str = None):
        # sourceId
        self.source_id = source_id
        # header Host
        self.host = host
        # 抓取开始页
        self.home_page = home_page
        self.category_list = {}
        # 类别选择器
        self.select_category = select_category
        # 类别总页数选择器
        self.select_category_page_count = select_category_page_count
        self.category_page_count = 0
        # 页面编码
        self.encoding = encoding
        # 自动抓取页面模板
        self.category_template = category_template
        # 单行小说列表信息
        self.select_novel_line = select_novel_line
        # 单行小说列表页名字选择器
        self.select_novel_name = select_novel_name
        # 单行小说作者选择器
        self.select_novel_author = select_novel_author
        # 小说目录url模板
        self.list_url_template = list_url_template
        # 封面选择器
        self.select_novel_cover = select_novel_cover
        # 标签选择器
        self.select_novel_tag = select_novel_tag
        # 简介选择器
        self.select_novel_introduction = select_novel_introduction
        # 章节选择器
        self.select_chapter = select_chapter
        # 章节内容选择器
        self.select_chapter_content = select_chapter_content

    # 获取分类列表
    # select 选定url的元素
    def __get_category_list(self):
        if self.encoding is None:
            self.encoding = "utf-8"
        homepage = SpiderTools.get_html(self.home_page, encoding=self.encoding)
        items = SpiderTools.get_pyquery_content(homepage, self.select_category)
        for item in items:
            url = PyQuery(item).attr("href")
            if not str(url).startswith("http"):
                url = self.host + url
            category = PyQuery(item).text()
            self.category_list[category] = url

    # 获取总页数，若没有则默认1500
    def __get_category_page_count(self, html):
        if self.select_category_page_count is None:
            self.category_page_count = 1500
        else:
            page_count = SpiderTools.get_pyquery_content(html, self.select_category_page_count)
            self.category_page_count = int(page_count)

    # 请重写
    def templet_format(self, target, current_category_key):
        raise ValueError("请重写此方法，以便生成自己的模板url")

    def chapter_url(self, target_url, mulu_url=None ):
        raise ValueError("请重写此方法，以便生成自己的章节url")

    # 小说列表简要信息保存
    def novel_simple_save(self):
        dbhelper = DBhelper(host="localhost", user='root', password='mysql', database='novels')
        self.__get_category_list()
        # 按类别循环获取
        for key in self.category_list:
            count = 0
            html = None
            templet = self.templet_format(self, key)
            if count == 0 and SpiderTools.getRes().category_template is not None:
                index_url = templet.format(1)
                html = SpiderTools.get_html(url=index_url, header_host=SpiderTools.getRes().host,
                                            encoding=SpiderTools.getRes().encoding,
                                            network_err_fn=SpiderTools.save_to_file("pageList.bak", index_url))
                if html is None:
                    continue
                self.__get_category_page_count(html)
            # 按页码循环列表
            for i in range(1, SpiderTools.getRes().category_page_count, 1):
                insertnovels = []
                if i != 1:
                    index_url = templet.format(i)
                    html = SpiderTools.get_html(url=index_url, header_host=SpiderTools.getRes().host,
                                                encoding=SpiderTools.getRes().encoding,
                                                network_err_fn=SpiderTools.save_to_file("pageList.bak", index_url))
                    if html is None:
                        continue
                novels = SpiderTools.get_pyquery_content(html, SpiderTools.getRes().select_novel_line)
                if len(novels) == 0:
                    break
                # 组装小说信息
                for item in novels:
                    novelname = SpiderTools.get_pyquery_content(item, SpiderTools.getRes().select_novel_name).text()
                    if novelname is None or novelname == '':
                        continue
                    url = SpiderTools.getRes().host + SpiderTools.get_pyquery_content(item,
                                                                                      SpiderTools.getRes().select_novel_name).attr(
                        "href")
                    author = \
                    SpiderTools.get_pyquery_content(item, SpiderTools.getRes().select_novel_author).text().split(" ")[0]
                    insertnovels.append(str((novelname, url, author, SpiderTools.getRes().source_id)))
                # 小说简要信息保存到数据库
                sql = "insert into novel (`name`,`source`,`author`,`sourceid`) values "
                sql = sql + ",".join(insertnovels) + " on DUPLICATE key update source = values(source)"
                dbhelper.update(sql)
                time.sleep(random.uniform(1, 3))

    # 小说详情信息保存
    def novel_detail_save(self):
        dbhelper = DBhelper(host="localhost", user='root', password='mysql', database='novels')
        tags = {}
        tag_list = dbhelper.query("SELECT id,`name` from dictionary where type = 'tag'")
        for _item in tag_list:
            tags[_item[1]] = _item[0]
        # 获取上一次更新的地址
        result = dbhelper.query_one(
            "SELECT novelId,chapterId from chapter ORDER BY novelId DESC,chapterId desc LIMIT 1")
        novelId = None
        start_chapter_index = None
        if result is not None:
            novelId = result[0]
            start_chapter_index = result[1]
        count = dbhelper.query_one("SELECT count(1) from novel")
        start, end, step = 0, int(count[0]), 500
        index_start = start
        if novelId is not None:
            start_novel_index = dbhelper.query_one("SELECT count(1) from novel where id <=%s", novelId)
            index_start = start + start_novel_index[0] - 1
        for i in range(start, end, step):
            values = dbhelper.query("select source,id,sourceid from novel limit %s,%s", (index_start, step))
            index_start = index_start + step
            if values is None or len(values) == 0:
                break
            for item in values:
                novel_home_url = item[0]
                novel_id = item[1]
                SpiderTools.sourceid = item[2]
                # 保存小说详细信息
                detail_fn = SpiderTools.save_to_file("detail.bak", novel_home_url + "," + str(novel_id))
                html = SpiderTools.get_html(novel_home_url, encoding=SpiderTools.getRes().encoding,
                                            network_err_fn=detail_fn)
                if html is None:
                    continue
                # 封面
                cover = SpiderTools.get_pyquery_content(html, SpiderTools.getRes().select_novel_cover).attr("src")
                # 类型
                tag = str(SpiderTools.get_pyquery_content(html, SpiderTools.getRes().select_novel_tag).text())[0:2]
                # 简介
                introduction = SpiderTools.get_pyquery_content(html,
                                                               SpiderTools.getRes().select_novel_introduction).text()
                # 此函式用于保存封面获取失败
                img_fn = SpiderTools.save_to_file("img.bak", cover + "," + str(novel_id))
                bconver = SpiderTools.get_html(cover, return_type="binary", network_err_fn=img_fn)
                # 获取tagId
                tag_id = 0
                for t in tags:
                    if str(t).find(tag) > -1:
                        tag_id = tags[t]
                        break
                dbhelper.update(" update novel set tagid = %s,introduction = %s,cover = %s where id = %s ",
                                (tag_id, introduction, bconver, novel_id))
                # 获取章节列表并保存
                self.get_chapters_save(novel_home_url + SpiderTools.getRes().list_url_template, novel_id,
                                       start_chapter_index)
            start_chapter_index = None

    # 简单保存章节来源，与生成章节id
    def get_chapters_save(self, url, novel_id, start_chapter_index):
        novel_mulu_fn = SpiderTools.save_to_file(file_name="novel_mulu.bak", save_text=url + "," + str(novel_id))
        html = SpiderTools.get_html(url, encoding=SpiderTools.getRes().encoding, network_err_fn=novel_mulu_fn)
        chapters = SpiderTools.get_pyquery_content(html, SpiderTools.getRes().select_chapter)
        dbhelper = DBhelper(host="localhost", user='root', password='mysql', database='novels')
        for chapter_id in range(0, len(chapters), 1):
            title = chapters.eq(chapter_id).text()
            source = self.chapter_url(SpiderTools.getRes(), chapters.eq(chapter_id).attr("href"), url)
            # source = str(url).replace(SpiderTools.getRes().list_url_template, "") + chapters.eq(chapter_id).attr("href")
            if start_chapter_index is not None and chapter_id <= start_chapter_index:
                continue
            sql = "INSERT into chapter (novelId,chapterId,title,source,sourceid) VALUES (%s,%s,%s,%s,%s)"
            dbhelper.update(sql, (novel_id, chapter_id + 1, title, source, SpiderTools.sourceid))

    # 抓取具体章节内容
    def novel_chapter_detail_save(self):
        dbhelper = DBhelper(host="localhost", user='root', password='mysql', database='novels')
        sql = "select novelId,chapterId,source,sourceid from chapter where flag = 0 limit 100"
        result = dbhelper.query(sql)
        while result is not None and len(result) > 0:
            updatesql = "update chapter set flag = 1 ,content = %s where novelId = %s and chapterId = %s"
            for item in result:
                novelId, chapterId, source, sourceid = item[0], item[1], item[2], item[3]
                SpiderTools.sourceid = sourceid
                html = SpiderTools.get_html(source, encoding=SpiderTools.getRes().encoding,
                                            header_host=SpiderTools.getRes().host)

                content = SpiderTools.get_pyquery_content(html, SpiderTools.getRes().select_chapter_content)
                content.remove("script")
                text = content.text().encode("utf-8", errors="ignore")
                zlib_chapter_text = zlib.compress(text)
                dbhelper.update(updatesql, (zlib_chapter_text, novelId, chapterId))
                time.sleep(random.uniform(1, 3))
            result = dbhelper.query(sql)

    # 开始抓取
    def start(self, flag):
        if flag == 1:
            # 小说简单详情
            self.novel_simple_save()
        if flag == 2:
            # 小说详情
            self.novel_detail_save()
        if flag == 3:
            self.novel_chapter_detail_save()