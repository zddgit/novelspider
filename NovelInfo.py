class Novel23us:
    __templateList = "https://www.23us.so/top/allvisit_%s.html"

    def __init__(self, pageCount):
        self.__pageCount = pageCount

    def getPageUrl(self, page=1):
        if page > self.__pageCount:
            raise ValueError("invalid value: %s" % page)
        return self.__templateList % page

    def setPageCount(self, pageCount):
        self.__pageCount = pageCount

