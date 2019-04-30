from pyquery import PyQuery

import MyTools as mytools


class NovelResource:
    # 构造函数
    def __init__(self, host, home_page, select_category):
        self.__host = host
        self.__homePage = home_page
        self.__category_list = {}
        self.__directory_template = ""
        self.__select_category = select_category

    # 获取分类列表
    # select 选定url的元素
    def get_category_list(self):
        homepage = mytools.get_html(self.__homePage)
        items = mytools.get_pyquery_content(homepage, self.__select_category)
        for item in items:
            url = PyQuery(item).attr("href")
            if not str(url).startswith("http"):
                url = str(self.__host).join(url)
            category = PyQuery(item).text()
            self.__select_category[category] = url

