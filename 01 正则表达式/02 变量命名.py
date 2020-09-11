# !/usr/bin/python3
# -*- coding:utf-8 -*- 
# author: Ming Luo
# time: 2020/9/11 11:16
import re

ret = "<h1>hahahah</h1>"
re.match(r'<(\w*)>.*</\1>', ret).group()

ret = "<body><h1>hahahah</h1></body>"
re.match(r"<(\w*)><(\w*)>.*</\2></\1>", ret).group()
# (?P<name>)   分组起别名      (?P=name)  引用别名为name分组匹配到的字符串
re.match(r"<(?P<p1>\w*)><(?P<p2>\w*)>.*</(?P=p2)></(?P=p1)>", ret).group()


def add(temp):
    str_num = temp.group()
    num = int(str_num) + 1
    return str(num)


# sub方法支持输入函数，将匹配的到值传入add中，并将add返回的值代替匹配到的值
ret = re.sub(r"\d+", add, "python = 997")
print(ret)
