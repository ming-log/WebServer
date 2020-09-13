# !/usr/bin/python3
# -*- coding:utf-8 -*-
# author: Ming Luo
# time: 2020/9/10 17:36

# 需求：
# 利用socket建立服务器，并且能够利用浏览器进行访问
# 要求多个浏览器可以同时访问
# epoll 仅在linux系统下才可运行

from socket import *
import re
import select


def work(client_socket, recv_data, epl, fd, fd_event_dict):
    if recv_data:
        # 解析请求的页面名字
        ret = r"^GET (/.*?) HTTP"
        page_name = re.findall(ret, recv_data)
        print('请求的页面为:', page_name)

        if page_name:
            page_name = page_name[0]
            if page_name == '/':
                page_name = "/index.html"  # 如果返回的是/，则让网址访问index.html
        # 打开文件操作及其危险，因此在此尝试打开文件
        try:
            # 拼接地址
            root_path = r'./html'  # 根目录
            complete_page_path = root_path + page_name  # 拼接
            # 打开页面，并读取内容
            f = open(complete_page_path, 'rb')  # 打开文件
        except:  # 如果打开文件失败，则返回404
            response_header = "HTTP/1.1 404 NOT FOUND\r\n"
            response_header += "\r\n"
            response_body = "------file not found-----\r\n"
            response = response_header + response_body
            client_socket.send(response.encode("utf-8"))
            client_socket.close()
            epl.unregister(fd)
            print("----close----")
            del fd_event_dict[fd]
        else:
            response_body = f.read()
            f.close()
            response_header = "HTTP/1.1 200 OK\r\n"
            response_header += "Content-Length:%d\r\n" % len(response_body)
            response_header += "\r\n"
            # body = "<h1>你好!</h1>\r\n"
            # return_data = response + body
            # 发送一些数据到客户端
            response = response_header.encode('utf-8') + response_body
            client_socket.send(response)
    else:
        client_socket.close()
        epl.unregister(fd)
        print("----close----")
        del fd_event_dict[fd]


def main():
    # 创建socket
    tcp_server_socket = socket(AF_INET, SOCK_STREAM)
    # 设置当服务器先close 即服务器端4次握手之后资源能够立即释放，这样就保证了，下次运行程序时，可以立即使用该端口
    tcp_server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # 本地信息
    address = ('', 8070)

    # 绑定
    tcp_server_socket.bind(address)

    # 使用socket创建的套接字默认的属性是主动的，使用listen将其变为被动的，这样就可以接收别人的链接了
    tcp_server_socket.listen(128)  # 允许很多客户端连接
    # 设置套接字为非堵塞
    tcp_server_socket.setblocking(False)

    # 创建一个epoll对象
    epl = select.epoll()

    # 将监听套接字对应的fd(文件描述符)注册到epoll中
    epl.register(tcp_server_socket.fileno(), select.EPOLLIN)

    fd_event_dict = dict()
    
    while True:
        fd_event_list = epl.poll()  # 默认会堵塞，直到os监测到数据到来  通过事件通知方式  告诉这个程序此时会解堵塞
        
        # [(fd, event), (套接字对应的文件描述符， 这个文件描述符到底是什么事件 例如可以调用recv接受等)]
        for fd, event in fd_event_list:
            if fd == tcp_server_socket.fileno():
                new_socket, client_addr = tcp_server_socket.accept()
                epl.register(new_socket, select.EPOLLIN)
                fd_event_dict[new_socket.fileno()] = new_socket
            elif event == select.EPOLLIN:
                # 判断已经链接的客户端是否有数据发送过来
                recv_data = fd_event_dict[fd].recv(1024).decode("utf-8")
                work(fd_event_dict[fd], recv_data, epl, fd, fd_event_dict)
    tcp_server_socket.close()


if __name__ == '__main__':
    main()
