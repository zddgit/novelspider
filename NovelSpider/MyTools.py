import requests
from pyquery import PyQuery
from requests import RequestException


# 获取url内容
# proxies 代理 proxies = {"http":"","https":""}
# network_err_fn 请求失败以后的处理函数
def get_html(url, proxies=None, network_err_fn=None, encoding="utf-8", return_type=None, host=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }
    if host is not None:
        headers["Host"] = host
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
            raise ValueError("url : %s ,status_code : %s" % url, response.status_code)
    except RequestException as e:
        print("network err")
        if network_err_fn is not None:
            network_err_fn()


# 从指定的文档获取指定元素内容包装为pyquery类型
def get_pyquery_content(doc, select):
    if isinstance(doc, PyQuery):
        return doc(select)
    else:
        doc = PyQuery(doc)
        return get_pyquery_content(doc, select)


# 从指定的文档获取需要的文本内容
def get_doc_text(pyquery_doc, fn):
    return fn(pyquery_doc)


if __name__ == "__main__":
    html = get_html("http://du1du.org/xuanhuanxiaoshuo/", encoding="gbk", host="du1du.org")
    pquery = get_pyquery_content(html, ".container .mb20 li a")


    def get1url(doc):
        return PyQuery(doc).eq(1).attr("href")


    print(str(get_doc_text(pyquery_doc=pquery, fn=get1url)).find("http"))
