#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

'''
针对多nginx配置，一次性添加或者修改
'''

## 游戏对应字典内容
ModeNameDict = {
	"Paigow":'8901',
	"Benzbmw":'8903',
	"Bjl":'8895',
	"Hhdz":'8890',
	"Bird":'8906',
	"Hongbao":'8900',
	"Lhd":'8898',
	"Lottery":'8904',
	"Qznn":'8893',
	"Shaibao":'8899',
	"Sumkung":'8902',
	"Ttz":'8896',
	"Zjh":'8897',
	"Zzl":'8905',
	"Brnn":'8894',
	"Pay":'8033',
	"Client":'8049',
	"ChatClient":'7499',
	"ChatServer":'7500',
	"ApiOrder":'9112'
}
## 定义变量
Note = ""
proxyPort=0000
listenPort=0000
proxyAddr="128.14.226.32"
serverName="hall.yin-d.com"
Platform="kknew"

## 按平台写nginx配置文件
def WebConfWriteFile(confName,Port,messages):
	try:

		#print(nginx_conf_template)
		handle = open(confName + '_' + str(Port) + '.conf','w')
		handle.write(messages)

	except IOError:
		print("info: 没有找到文件或读取文件失败")
		return json.dumps({'status': 500, 'resultInfo': 'Nginx config template write fail'})

	else:
		print("info: 文件内容写入文件成功")
		handle.close()
		return json.dumps({'status': 200, 'resultInfo': 'Nginx config template write success'})

### 重新加载变量；写入配置文件
for key in ModeNameDict:
	print("Write " + key + ":" + ModeNameDict[key])
	Note = key
	listenPort = int(ModeNameDict[key])

	## 配置文件模板
	nginx_conf_template = '''## http
server {{
	### {notes}
	listen {port};
	server_name {servername};
	charset UTF-8;
	access_log /data/logs/{dirname}_{notes}_{port}.log nginx-py;
	
	# set site Angent
	if ($http_user_agent ~* "qihoobot|Baiduspider|Googlebot|Googlebot-Mobile|Googlebot-Image|Mediapartners-Google|Adsbot-Google|Feedfetcher-Google|Yahoo! Slurp|Yahoo! Slurp China|YoudaoBot|Sosospider|Sogou spider|Sogou web spider|MSNBot|ia_archiver|Tomato Bot") {{
	return 403;
	}}
	
	# set site host
	#if ( $host != '{servername}' ) {{ return 403; }}
	
	# set site favicon
	location /favicon.ico {{ return 404; }}
	
	location / {{
	index index.html index.htm;
	proxy_pass http://{proxy_ip}:{proxy_port};
	proxy_set_header X-Real-IP $remote_addr;
	proxy_set_header Upgrade $http_upgrade;
	proxy_set_header Connection $connection_upgrade;
	}}
	}}
	'''.format(
	notes = Note,
	port=listenPort,
	servername=serverName,
	dirname=Platform,
	access_log=serverName,
	proxy_port=listenPort,
	proxy_ip=proxyAddr
	)

	WebConfWriteFile(Note,listenPort,nginx_conf_template)键入消息
