class Novel23us:
    # https://www.x23us.com/html/66/66656/
    __templateList = "https://www.23us.so/top/allvisit_%s.html"
    __templateDetail = "https://www.23us.so/xiaoshuo/{}.html"

    def __init__(self, page_count):
        self.__pageCount = page_count

    def get_page_url(self, page=1):
        if page > self.__pageCount:
            raise ValueError("invalid value: %s" % page)
        return self.__templateList % page

    def get_detail_url(self, source_id):
        return self.__templateDetail.format(source_id)

    def set_page_count(self, page_count):
        self.__pageCount = page_count
