# !/usr/bin/python3
# -*- coding:utf-8 -*- 
# author: Ming Luo
# time: 2020/9/10 17:34

# 需求：
# 利用socket建立服务器，并且能够利用浏览器进行访问
# 要求多个浏览器可以同时访问

from socket import *
import threading


def work(client_socket, client_addr):
    while True:
        # 接收对方发送过来的数据
        print(client_socket)
        print(client_addr)
        recv_data = client_socket.recv(1024).decode("gbk")  # 接收1024个字节
        # 如果recv解堵塞，那么有2种方式:
        # 1. 客户端发送过来数据
        # 2. 客户端调用close导致，这里recv解堵塞recv_data将为空
        if not recv_data:
            break
        print('接收到的数据为:\n', recv_data)

        return_data = "HTTP/1.1 200 OK\n\n<h1>你好!</h1>"
        # 发送一些数据到客户端
        client_socket.send(return_data.encode('gbk'))
    print('---- 客户%s服务完毕 ----' % str(client_addr))
    # 关闭为这个客户端服务的套接字,只要关闭了，就意味着不能再为这个客户端服务了，如果还需要服务，只能再次访问
    client_socket.close()

def main():
    # 创建socket
    tcp_server_socket = socket(AF_INET, SOCK_STREAM)

    # 本地信息
    address = ('127.0.0.1', 8070)

    # 绑定
    tcp_server_socket.bind(address)

    # 使用socket创建的套接字默认的属性是主动的，使用listen将其变为被动的，这样就可以接收别人的链接了
    tcp_server_socket.listen(128)  # 允许很多客户端连接

    while True:
        # 监听套接字 负责 等待有新的客户端进行连接
        # accept产生的新的套接字用来 为客户端服务
        client_socket, client_addr = tcp_server_socket.accept()
        t = threading.Thread(target=work, args=(client_socket, client_addr))
        t.start()
    t.join()
    tcp_server_socket.close()


if __name__ == '__main__':
    main()
