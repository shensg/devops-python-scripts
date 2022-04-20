#!/usr/bin/env python3
# --*--coding:utf-8--*--
# Author: Shensg

import requests
import time
from requests.auth import HTTPBasicAuth

# 获取nsq所有topic
def delUnusedTopicAndChannel(addr):
    f = requests.get(addr, auth=HTTPBasicAuth(username, password))
    f = f.json()
    # print("所有topic")
    # print(f)
    topicList = f.get("topics", None)
    for topic in topicList:
        time.sleep(0.01)
        r = requests.get(addr + "/" + topic, auth=HTTPBasicAuth(username, password))
        # r = requests.request("GET", addr + "/" + "production.live_event_push")
        # print(r.json)
        data = r.json()
        #print(data)
        l = data.get("nodes", None)[0]
        print(l.get("channels", None))
        if len(l.get("channels", None)):
            # 删除无用的channel
            res = l.get("channels", None)
            for i in res:
                """
                这是删除nsq：v1.2.0 的topic和channel
                """
                if i.get("client_count") == 0:
                    print("删除无用channel", i.get("topic_name", None), i.get("channel_name", None))
                    r1 = requests.delete(addr + "/" + i.get("topic_name", None) + "/" + i.get("channel_name", None), auth=HTTPBasicAuth(username, password))
                    print(r1)
                    time.sleep(0.1)
                """
                这是删除nsq：v1.1.0 的topic和channel
                """
                if not i.get("clients"):
                    print("删除无用channel", i.get("topic_name", None), i.get("channel_name", None))
                    r1 = requests.delete(addr + "/" + i.get("topic_name", None) + "/" + i.get("channel_name", None), auth=HTTPBasicAuth(username, password))
                    print(r1)
                    time.sleep(0.1)
        else:
            # 删除无用的topic
            print("删除无用topic", l.get("topic_name", None))
            r1 = requests.delete(addr + "/" + l.get("topic_name", None), auth=HTTPBasicAuth(username, password))
            print(r1)
            time.sleep(0.1)

if __name__ == "__main__":
    username = "ydjadmin"
    password = ""
    addr = "https://<doamin.com>/api/topics"
    delUnusedTopicAndChannel(addr)
    delUnusedTopicAndChannel(addr)

