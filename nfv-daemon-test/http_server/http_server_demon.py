# -- coding: utf-8 --
import socket
import ssl
import re
import json
import datetime
from multiprocessing import Process
import os
# https server服务器，用于模拟PIM服务,适配置IPV6
os.getcwd()
class HTTPServer(object):
    def __init__(self):
        self.context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        self.context.load_cert_chain(certfile='cert.pem',keyfile='key.pem')
        self.server_socket = socket.socket(socket.AF_INET6) #AF_INET为IPV4,AF_INET6为IPV6

    def start(self):
        self.server_socket.listen(128)
        while True:
            client_socket, client_address = self.server_socket.accept()
            print "POST address:",client_address
            client_socket = self.context.wrap_socket(client_socket,server_side=True)
            handle_client_process = Process(target=self.handle_client, args=(client_socket,))
            handle_client_process.start()
            client_socket.close()

    def bind(self, port):
        self.server_socket.bind(("", port))

#####################################################################################

    def date_time(self):
        time = datetime.datetime.now().replace(microsecond=0)
        return time

    def pim_login(self):
        #返回登录报文,带Body
        print "*"*50+"pim login response:"+str(datetime.datetime.now().replace(microsecond=0))+"*"*50
        expiresat = (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).replace(microsecond=0).isoformat() + '.000Z'
        body = {
            "Token": "gAAAAABZJ8a7aiq1SnOhbNw8vFb5WZC",
            "IssuedAt": "2018-08-03T00:00:00.000Z",
            "ExpiresAt": expiresat,
            "CallBackUris": [
                {
                    "UriType": "dsmCm",
                    "CallBackUri": "https://10.252.90.3:8000/dsmCm"
                },
                {
                    "UriType": "dsmPm",
                    "CallBackUri": "https://10.252.90.3:8000/dsmPm"
                },
                {
                    "UriType": "dsmLog",
                    "CallBackUri": "https://10.252.90.3:8000/dsmLog"
                }]
        }
        response_start_line = "HTTP/1.1 201 OK\r\n"
        response_headers = "Content-Type: application/json; charset=UTF-8\r\n"
        response_body = json.dumps(body)
        response = response_start_line + response_headers + "\r\n" + response_body
        return response

    def error(self):
        body = {
            "error":"param is invild!!!"
        }
        response_start_line = "HTTP/1.1 400 OK\r\n"
        response_headers = "Content-Type: application/json; charset=UTF-8\r\n"
        response_body = json.dumps(body)

        response = response_start_line + response_headers + "\r\n" + response_body
        return response

    def success(self):
        #返回成功，不带Body
        print "*" * 50 + "log cm pm response:"+str(datetime.datetime.now().replace(microsecond=0)) + "*" * 50
        response_start_line = "HTTP/1.1 201 OK\r\n"
        response_headers = "Content-Type: application/json; charset=UTF-8\r\n"
        # response_body = json.dumps(body)

        response = response_start_line + response_headers+ "\r\n"
        return response
    def handle_client(self, client_socket):
        """
        处理客户端请求
        """
        # 获取客户端请求数据
        try:
            request_data = client_socket.recv(1024)
            request_lines = request_data.splitlines()
            # print "request_data:",request_data
            # 解析请求报文
            parameter = request_lines[0].split()[1]

            print "parameter:",parameter
            if parameter == '/tokens':
                print "*" * 50 + "pim login request:"+ str(datetime.datetime.now().replace(microsecond=0)) + "*" * 50
                print request_lines
                response = self.pim_login()
                print response
            elif parameter == '/dsmCm' or parameter == '/dsmPm' or parameter == '/dsmLog':
                print "*" * 50 + "cm pm log request:"+ str(datetime.datetime.now().replace(microsecond=0)) + "*" * 50
                print request_lines
                response = self.success()
                print response
            else:
                response = self.error()
            # 向客户端返回响应数据
            client_socket.send(response)
        except Exception,ex:
            print ex

        # 关闭客户端连接
        client_socket.close()

def main():
    http_server = HTTPServer()
    http_server.bind(8000)
    http_server.start()


if __name__ == "__main__":
    main()