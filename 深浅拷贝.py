# !/usr/bin/python3
# -*- coding:utf-8 -*- 
# author: Ming Luo
# time: 2020/9/14 16:55
import copy

# 1. =
a = [11, 22, [33, 44]]  # 实际上是a指向列表保存的地址
b = a  # 使b也指向列表保存的地址
print(id(a) == id(b))  # 此时a，b的保存地址相同
a.append(123)   # 此时往a所指向的列表添加123这个元素a和b都会发生变化
print(a)
print(b)

# 2. copy 浅拷贝
a = [11, 22, [33, 44]]  # 实际上是a指向列表保存的地址
b = copy.copy(a)  # 重新开辟一块地址将列表拷贝一份保存下来，并且使b指向保存后的列表
print(id(a) == id(b))  # 此时a，b的保存地址不同
a.append(123)   # 此时往a所指向的列表添加123这个元素,b不会发生变化
print(a)  # [11, 22, [33, 44], 123]
print(b)  # [11, 22, [33, 44]]

# 但是往列表中的子列表添加元素会导致b也发生变化
# 因为列表中的列表，实际上是在列表中保存的子列表的内存地址
# 当进行浅拷贝的时候，只是将a中的第一层拷贝给了b
# 也就是说列表中的子列表在内存中的地址是一样的
a = [11, 22, [33, 44]]  # 实际上是a指向列表保存的地址
b = copy.copy(a)  # 重新开辟一块地址将列表拷贝一份保存下来，并且使b指向保存后的列表
print(id(a[2]) == id(b[2]))  # 此时a[2]，b[2]的内存地址相同
a[2].append(123)   # 此时往a[2]所指向的列表添加123这个元素,b也会发生变化
print(a)  # [11, 22, [33, 44], 123]
print(b)  # [11, 22, [33, 44], 123]

# 深拷贝,完全开辟列表中所有元素的存储地址,与源列表毫无关系
a = [11, 22, [33, 44]]  # 实际上是a指向列表保存的地址
b = copy.deepcopy(a)  # 完全重新开辟列表中所有元素的存储地址,与源列表毫无关系
print(id(a[2]) == id(b[2]))  # 此时a[2]，b[2]的内存地址不同
a[2].append(123)   # 此时往a[2]所指向的列表添加123这个元素,b不会发生变化
print(a)  # [11, 22, [33, 44], 123]
print(b)  # [11, 22, [33, 44]]

a = [11, 22]
b = [33, 44]
c = (a, b)
d = [a, b]
id(a)
id(b)
id(c)
id(d)
a.append(1)
e = copy.copy(c)
f = copy.copy(d)
id(e)
id(f)



a = (1, 2, 3)
b = [1, 2, 3]
id(a)
id(b)
c = copy.copy(a)
d = copy.copy(b)
id(c)
id(d)
