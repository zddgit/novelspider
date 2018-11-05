import zlib
import NovelSpider


s = NovelSpider.get_chapter_text("https://www.23us.so/files/article/html/14/14239/6201207.html", 14239, 86)
b = s.encode(encoding="GBK", errors="ignore")
zlib_s = zlib.compress(b)
print(len(b))
print(len(zlib_s))
b1 = zlib.decompress(zlib_s)
s1 = b1.decode("GBK")
print(s1)


