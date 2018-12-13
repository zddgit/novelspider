import random
import time

import NovelSpider as ns

regions = {"吉林", "辽宁", "北京", "河南", "山东", "黑龙江"}


def isNeed(address, regions):
    for region in regions:
        if region in address:
            return True
    return False


def getIpList(pagecount, protocol, regions):
    page = 1
    while page <= pagecount:
        daili = "http://www.xicidaili.com/nn/%s" % page
    text = ns.get_html(daili)
    page = page + 1
    els = ns.get_content(text, "#ip_list .odd")
    for el in els:
        items = ns.get_content(el, "td")
        protocol_ = items.eq(5).text()
        address = items.eq(3).text()
        timeout = items.eq(6)("div").attr("title")
        if protocol_ == protocol and isNeed(address, regions) and float(timeout.replace("秒", "")) < 1:
            print(address)
            ip = items.eq(1).text()
            port = items.eq(2).text()
            print(ip + ":" + port)
    time.sleep(random.uniform(1, 3))
