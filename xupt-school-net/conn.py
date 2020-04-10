#!/usr/bin/local/python3
# -*-coding:utf8-*-

import urllib.request
import urllib.parse

def regist(username, passwd):
    url = 'http://172.18.0.3'  # 校园网登陆验证页面
    postdata = urllib.parse.urlencode({
        'DDDDD': str(username),
        'upass': str(passwd),
        'R1': 0,
        'R2': '',
        'R6': 0,
        'para': 00,
        '0MKKey': '123456',
        'buttonClicked': '',
        'redirect_url': '',
        'err_flag': '',
        'username': '',
        'password': '',
        'user':'' ,
        'cmd':'' ,
        'Login': ''
    }).encode('utf-8')

    req = urllib.request.Request(url, postdata)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3528.4 Safari/537.36')


if __name__ == '__main__':
    username = ""
    passwd = ""
    regist(username, passwd)
