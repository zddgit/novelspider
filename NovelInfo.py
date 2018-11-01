class Novel23us:
    # https://www.x23us.com/html/66/66656/
    __templateList = "https://www.23us.so/top/allvisit_%s.html"
    __templateDetail = "https://www.23us.so/xiaoshuo/{}.html"

    def __init__(self, pageCount):
        self.__pageCount = pageCount

    def getPageUrl(self, page=1):
        if page > self.__pageCount:
            raise ValueError("invalid value: %s" % page)
        return self.__templateList % page

    def get_detail_url(self, source_id):
        return self.__templateDetail.format(source_id)

    def setPageCount(self, pageCount):
        self.__pageCount = pageCount
