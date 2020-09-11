# !/usr/bin/python3
# -*- coding:utf-8 -*- 
# author: Ming Luo
# time: 2020/9/10 17:33

import re


def main():
    ret = '^[a-zA-Z0-9_]{4,20}@163.com'
    email_list = ['123@163.com', 'avdcjsdhjwe@163.com', '1234@163.com', '1234@.com', '12340@162.com', '.1234@163.com']
    for i in email_list:
        rt = re.match(ret, i)
        if rt:
            print('%s 匹配成功' % i)
        else:
            print('%s 匹配失败' % i)



if __name__ == '__main__':
    main()





