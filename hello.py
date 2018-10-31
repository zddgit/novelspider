import sys
import re
from enum import Enum, unique
import requests
from bs4 import BeautifulSoup


class Student:
    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def getName(self):
        return self.__name


bart = Student("zdd", 99)
print(bart.getName())
print(isinstance(bart, Student))
print(type(bart))
print(type(bart) == Student)
print(dir(Student))
print(max)
# Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
# for name, member in Month.__members__.items():
#     print(name, '=>', member, ',', member.value)
print(sys.path)


@unique
class Weekday(Enum):
    Sun = 0  # Sun的value被设定为0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6


for name, member in Weekday.__members__.items():
    print(name, '=>', member, ',', member.value)

print(type(Student))
hello = type('Student1', (Student,), {})
print(hello.getName(bart))
m = re.match(r'^(\d+?)(0*)$', '102300')
print(m.group(0))
print(m.group(1))
print(m.group(2))
# with open() as f:
#     lines = f.readlines()


print(re.search(r'([0-9]+)\.html', "https://www.23us.so/xiaoshuo/14239.html").group(1))
