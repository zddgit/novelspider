import zlib
import OldNovelSpider
import base64
from RedisHelper import RedisHelper

# s = NovelSpider.get_chapter_text("https://www.23us.so/files/article/html/14/14239/6201207.html", 14239, 86)
# b = s.encode(encoding="GBK", errors="ignore")
# zlib_s = zlib.compress(b)
# print(len(b))
# print(len(zlib_s))
# b1 = zlib.decompress(zlib_s)
# s1 = b1.decode("GBK")
# print(s1)
redis_helper = RedisHelper()
cover = "https://www.23us.so/files/article/image/29/29702/29702s.jpg"
imgfn = OldNovelSpider.save_to_file(file_name="img.bak", save_text=cover + "," + str(121))
bimg = OldNovelSpider.get_html(cover, return_type="binary", fn=imgfn)
print(len(bimg))
zlib_a = zlib.compress(bimg)
print(len(zlib_a))
# redis_helper.get_redis().set("image_{}".format(0), bimg)
