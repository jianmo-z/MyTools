#!/usr/bin/python3
# -*- coding:utf-8 -*-
import base64
import datetime
import json
import os
import random
import subprocess
import sys
import traceback

import time
from functools import wraps
from urllib import request

# 订阅链接地址
uri = ""
config_path = "/etc/v2ray/config.json"
scripts_log = "/opt/scripts/scripts.log"

green = "\033[0;32m"  # green
red = "\033[1;31m"  # red
reset = "\033[0m"  # reset

LOG_ERR = 0
LOG_INFO = 1
LOGDIC = {
	LOG_ERR: red + "error" + reset,
	LOG_INFO: green + "info" + reset,
}


# 改变终端字的颜色
def get_red(info):
	if isinstance(info, str) or isinstance(info, bytes):
		if isinstance(info, bytes):
			info = info.decode("utf-8")
		return red + info + reset
	else:
		return info


# 改变终端字的颜色
def get_green(info):
	if isinstance(info, str) or isinstance(info, bytes):
		if isinstance(info, bytes):
			info = info.decode("utf-8")
		return green + info + reset
	else:
		return info


# 写日志
def log(log_type, funcname, message):
	with open(scripts_log, "a+") as fd:
		fd.write("{} [{}] => {}:{}\n".format(datetime.datetime.now(), LOGDIC[log_type], funcname, message))


# 日志装饰器
def logger(funcname):
	def task(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			log(LOG_INFO, funcname, "begin to run...")
			try:
				return func(*args, **kwargs)
			except Exception as e:
				log(LOG_ERR, funcname, traceback.print_exc())
				exit(0)
			finally:
				log(LOG_INFO, funcname, "run to end...")
		return wrapper
	return task


# 获取订阅信息
@logger("get_subscription")
def get_subscription(uri, code=True):
	"""
	当code为Ture返回str，否则返回bytes类型
	:param uri:
	:param code:
	:return:
	"""
	user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) \
AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/76.0.3809.132 Safari/537.36"
	try:
		req = request.Request(uri)
		req.add_header('User-Agent', user_agent)
		res = request.urlopen(req).read()
	except Exception as e:
		log(LOG_ERR, "get_subscription", e)
	# print(e)
	if code:
		res = res.decode("utf-8")
	return res


# 解析订阅信息
@logger("parse_subscription")
def parse_subscription(Subscription):
	res = base64.b64decode(Subscription + '=' * (4 - len(Subscription) % 4))
	res = res.decode("utf-8")
	vmesses = res.splitlines()
	return vmesses


# 解析vmess为json
@logger("parse_vmess")
def parse_vmess(vmess, code=True):
	vmess = vmess[8:]
	if vmess[-1] == "=" or not (len(vmess) % 4):
		config = base64.b64decode(vmess)
	else:
		config = base64.b64decode(vmess + '=' * (4 - len(vmess) % 4))
	if code:
		config = config.decode("utf-8")
	return config


# json反序列化
@logger("load_config")
def load_config(config):
	return json.loads(config)


# 写入配置文件
@logger("write2config")
def write2config(config):
	# print(config)
	with open(config_path, "r+") as fd:
		oldConfig = json.loads(fd.read())

		outbounds = oldConfig['outbounds'][0]
		settings = outbounds['settings']
		streamSettings = outbounds['streamSettings']

		vnext_item = settings['vnext'][0]
		vnext_item["address"] = config["add"]
		vnext_item["port"] = int(config["port"])
		vnext_item["users"][0]['id'] = config["id"]
		vnext_item["users"][0]['alterId'] = config["aid"]
		streamSettings['network'] = config['net']
		streamSettings['tlsSettings']['serverName'] = config['host']
		if config['net'] == 'ws':
			streamSettings['wsSettings']['headers'] = {"Host": config['host']}
			streamSettings['wsSettings']['path'] = config['path']

		outbounds['settings'] = settings
		outbounds['streamSettings'] = streamSettings
		oldConfig['outbounds'][0] = outbounds

		# 清空文件内容，重新写入
		fd.seek(0)
		fd.truncate()
		fd.write(json.dumps(oldConfig, indent=4))


# 测试是否可以连接
@logger("is_reachable")
def is_reachable(ip, times=3, timeout=3, count=1):
	with open(scripts_log, "a+") as fd:
		for i in range(int(times)):
			ret = subprocess.Popen("ping -c {} -W {} {}".format(count, timeout, ip), shell=True, stdout=fd, stderr=fd)
			try:
				ret.wait(3)  # 等待三秒
			except Exception as e:
				log(LOG_ERR, "is_reachable", e)
			if ret.returncode == 0:
				return True
			else:
				time.sleep(1)

	return False


# restart v2ray
@logger("restart v2ray")
def restart_v2ray(times):
	log(LOG_INFO, "restart_v2ray", "begin restart v2ray...")
	with open(scripts_log, "a+") as fd:
		for i in range(int(times)):
			ret = subprocess.Popen("systemctl restart v2ray", shell=True, stdout=fd, stderr=fd)
			ret.wait(10)  # 等待十秒
			if ret.returncode == 0:
				log(LOG_INFO, "restart_v2ray", "success restarted v2ray...")
				return
			else:
				time.sleep(3)
		log(LOG_INFO, "restart_v2ray", "fail to  restart v2ray...")


# 自动更新配置信息
def update_config():
	# 从订阅服务器获取
	subscription = get_subscription(uri, True)

	# 解析订阅服务器
	vmesses = parse_subscription(subscription)

	# 解析节点配置信息
	serveres = list()
	for v in vmesses:
		config = parse_vmess(v)
		serveres.append(load_config(config))

	# 找一个可用的节点重新生成配置文件
	# with open(scripts_log, "r+") as fd:
	for it in serveres:
		if is_reachable(it['add']):
			log(LOG_INFO, "update_config", "ping {} success".format(it['add']))
			write2config(it)
			if os.system("systemctl restart v2ray"):
				log(LOG_ERR, "update_config", " failed to restart v2ray.service")
			return
		else:
			log(LOG_ERR, "update_config", "ping {} failed".format(id['add']))
	# 没有一个节点能用
	log(LOG_ERR, update_config, "no server can be use")
	exit(1)


# 初始化
def init():
	# 创建文件
	if not os.path.isfile(scripts_log):
		os.system("touch {}".format(scripts_log))


if __name__ == "__main__":
	init()  # 初始化

	cmd = 'curl -x socks5://127.0.0.1:1080 -I -m 10 -o /dev/null -s -w %{http_code} www.google.com'
	time.sleep(10)

	while True:
		res = os.popen(cmd).read()
		if res == "200":  # 可以访问google
			# 十分钟到三十五分钟
			seconds = 60 * random.randint(10, 15) + random.randint(1, 300)
			log(LOG_INFO, "main", "can access google, ready to sleep {} seconds ... ".format(seconds))
			time.sleep(seconds)  # 等待n久后重测，与google的链接
		else:
			log(LOG_ERR, "main", "can't access google, update config ...")
			update_config()  # 更新配置信息
			log(LOG_INFO, "main", "update success")
			restart_v2ray(3)  # 重新启动v2ray
