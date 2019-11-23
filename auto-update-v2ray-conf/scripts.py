#!/usr/bin/python3
# -*- coding:utf-8 -*-
import base64
import json
import os
import random
import subprocess
import logging
import time
from urllib import request

# 配置信息
url = ""
config_path = "/etc/v2ray/config.json"
scripts_log = "/opt/scripts/scripts.log"
logging.basicConfig(filename=scripts_log, format="%(asctime)s-%(name)s-%(levelname)s-%(message)s", level=logging.INFO)

green = "\033[0;32m"  # green
red = "\033[1;31m"  # red
reset = "\033[0m"  # reset


# 获取订阅信息
def get_subscription(url, code=True):
	"""
	当code为Ture返回str，否则返回bytes类型
	:param url:
	:param code:
	:return:
	"""
	user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) \
AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/76.0.3809.132 Safari/537.36"
	try:
		req = request.Request(url)
		req.add_header('User-Agent', user_agent)
		result = request.urlopen(req).read()
	except Exception as e:
		pass
	if code:
		result = result.decode("utf-8")
	return result


# 解析订阅信息
def parse_subscription(Subscription):
	result = base64.b64decode(Subscription + '=' * (4 - len(Subscription) % 4))
	result = result.decode("utf-8")
	vmesses = result.splitlines()
	return vmesses


# 解析vmess为json
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
def load_config(config):
	return json.loads(config)


# 写入配置文件
def write2config(config):
	with open(config_path, "r+") as fd:
		server_config = json.loads(fd.read())
		server_config['outbounds'][0]['settings']['vnext'][0]['address'] = config['add']  # address
		server_config['outbounds'][0]['settings']['vnext'][0]['port'] = int(config['port'])  # port
		server_config['outbounds'][0]['settings']['vnext'][0]['users'][0]['id'] = config['id']  # id
		server_config['outbounds'][0]['streamSettings']['wsSettings']['headers']['Host'] = config['host']  # host
		server_config['outbounds'][0]['streamSettings']['wsSettings']['path'] = config['path']  # path
		server_config['outbounds'][0]['streamSettings']['tlsSettings']['serverName'] = config['host']  # serverName
		server_config['outbounds'][0]['streamSettings']['network'] = config['net']  # network

		# 清空文件内容，重新写入
		fd.seek(0)
		fd.truncate()
		fd.write(json.dumps(server_config, indent=4))


# 测试是否可达
def is_reachable(ip, times=3, timeout=3, count=1):
	for i in range(int(times)):
		try:
			ret = subprocess.Popen("ping -c {} -W {} {}".format(count, timeout, ip), shell=True)
			ret.wait(3)  # 等待三秒
		except Exception as e:
			# log(LOG_ERR, "is_reachable", e)
			logging.error("{} is unreachable".format(ip))
		if ret.returncode == 0:
			logging.info("{} is reachable".format(ip))
			return True
		else:
			time.sleep(1)
	return False


# 测试是否可访问Google
def is_accessable():
	command = 'curl -x socks5://127.0.0.1:1080 -I -m 10 -o /dev/null -s -w %{http_code} www.google.com'
	ret = os.popen(command).read()
	return True if ret == "200" else False


# restart v2ray
def restart_v2ray(times=3):
	logging.info("restart v2ray service")
	with open(scripts_log, "a+") as fd:
		for i in range(int(times)):
			ret = subprocess.Popen("systemctl restart v2ray || systemctl start v2ray", shell=True, stdout=fd, stderr=fd)
			ret.wait(10)  # 等待十秒
			if ret.returncode == 0:
				logging.info("success restarted v2ray")
				return True
			else:
				logging.error("failed to restart v2ray retries {}/{}".format(i + 1, times))
				time.sleep(2)
	return False


# 自动更新配置信息
def update_config():
	# 从订阅服务器获取
	subscription = get_subscription(url, True)

	# 解析订阅服务器
	vmesses = parse_subscription(subscription)

	# 解析节点配置信息
	serveres = list()
	for v in vmesses:
		config = parse_vmess(v)
		serveres.append(load_config(config))

	# 找一个可用的节点重新生成配置文件
	for it in serveres:
		if is_reachable(it['add']):  # 测试是否可达
			logging.info("{} is reachable".format(it['add']))
			write2config(it)  # 写入配置文件
			restart_v2ray(3)  # 重新启动v2ray
			time.sleep(10)  # 等待v2ray.service重启起来
			if is_accessable():  # 测试是否可以访问google
				return
			logging.info("{} can't use for access google".format(it['add']))
		else:
			logging.info("try other server")
			time.sleep(1)

	logging.info("no server can be used, exit")
	exit(1)


# 初始化
def init():
	# 创建文件
	if not os.path.isfile(scripts_log):
		os.system("touch {}".format(scripts_log))


if __name__ == "__main__":
	# init()  # 初始化

	while True:
		if is_accessable():  # 可以访问google
			# 三十分钟到六十分钟睡眠
			seconds = 60 * random.randint(30, 50) + random.randint(1, 600)
			logging.info("can access google, ready to sleep {} seconds".format(seconds))
			time.sleep(seconds)  # 等待n久后，重测与google的链接
		else:
			logging.error("can't access google, try other server")
			update_config()  # 更新配置信息
			logging.info("success update v2ray config")

