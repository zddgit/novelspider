import requests
from pyquery import PyQuery
from requests import RequestException
from NovelSpider.NovelRes import NovelResource

# 具体使用的来源信息
resource = {}
# 运行期间数据来源
sourceid = 0
# 运行期间要插入的表
table_name = {}
# 运行期间对应表所存在的数据总量
total = {}
# 分表创建表的语句
creat_chapter_sql = '''
CREATE TABLE `chapter_%s_%s` (
  `novelId` int(11) NOT NULL,
  `chapterId` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `source` varchar(255) DEFAULT NULL COMMENT '目标url',
  `content` blob,
  `sourceid` int(2) DEFAULT NULL COMMENT '来源',
  `flag` int(1) DEFAULT '0' COMMENT '0：未更新内容，1:更新了',
  PRIMARY KEY (`novelId`,`chapterId`) USING BTREE,
  KEY `index_novelId` (`novelId`) USING BTREE,
  KEY `chapter_flag_idx` (`flag`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''


def addRes(key: int, value: NovelResource):
    resource[key] = value


def getRes():
    return resource.get(sourceid)


# 获取url内容
# proxies 代理 proxies = {"http":"","https":""}
# network_err_fn 请求失败以后的处理函数
def get_html(url: str, proxies=None, network_err_fn=None, encoding="utf-8", return_type=None, header_host=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }
    if header_host is not None:
        headers["Host"] = header_host
    if not (url.startswith("https") or url.startswith("http")):
        url = "http://" + url
    try:
        if proxies is None:
            print("don't pass proxies")
            response = requests.get(url=url, headers=headers, timeout=3.0)
        else:
            print("pass proxies")
            response = requests.get(url=url, headers=headers, timeout=10.0, proxies=proxies)
        if response.status_code == 200:
            response.encoding = encoding
            if return_type == "text" or return_type is None:
                return response.text
            if return_type == "binary":
                return response.content
            else:
                raise ValueError("return_type only uses `text`, `binary` two options")
        else:
            raise ValueError("url : %s ,status_code : %s" % (url, response.status_code))
    except BaseException as e:
        print("network err,{}".format(e))
        if network_err_fn is not None:
            network_err_fn()


# 从指定的文档获取指定元素内容包装为pyquery类型
def get_pyquery_content(doc, select):
    if isinstance(doc, PyQuery):
        if select is not None:
            return doc(select)
        else:
            return doc
    else:
        doc = PyQuery(doc)
        return get_pyquery_content(doc, select)


# pageList.bak 小说列表页面网址
# detail.bak   小说详情 + 小说源id
# img.bak      小说封面网址 + 小说源id
# detail_list.bak  小说章节目录的网址 + 小说源id
# chapter.bak  小说具体章节页面网址 + 小说源id + 章节id
# r 读模式 w 写文件  a 追加
def save_to_file(file_name, save_text):
    def fn():
        if file_name is not None:
            with open(file_name, "a") as f:
                f.write(save_text + "\n")
                f.close()

    return fn


if __name__ == '__main__':

    html = get_html("http://www.quanwenyuedu.io/n/aoshidanshen/xiaoshuo.html")
    tag = get_pyquery_content(html, ".top p:eq(2) span").text()
    print(tag)
