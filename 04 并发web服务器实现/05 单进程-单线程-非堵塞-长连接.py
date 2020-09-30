# !/usr/bin/python3
# -*- coding:utf-8 -*-
# author: Ming Luo
# time: 2020/9/10 17:36

# 需求：
# 利用socket建立服务器，并且能够利用浏览器进行访问
# 要求多个浏览器可以同时访问

from socket import *
import re


def work(client_socket_list):
    for client_socket in client_socket_list:
        try:
            recv_data = client_socket.recv(1024)
        except:
            pass
        else:
            if recv_data:
                # 接收对方发送过来的数据
                recv_data = recv_data.decode("gbk")  # 接收1024个字节
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
                    print("----close----")
                    client_socket_list.remove(client_socket)
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
                print("----close----")
                client_socket_list.remove(client_socket)


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

    client_socket_list = []
    while True:
        # 监听套接字 负责 等待有新的客户端进行连接
        # accept产生的新的套接字用来 为客户端服务
        try:
            new_socket, client_addr = tcp_server_socket.accept()
            print("------create socket------")
        except Exception as e:
            pass
        else:
            # 设置套接字为非堵塞
            new_socket.setblocking(False)
            client_socket_list.append(new_socket)
        work(client_socket_list)

    tcp_server_socket.close()


if __name__ == '__main__':
    main()
