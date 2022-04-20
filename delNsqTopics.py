#!/usr/bin/env python3
# --*--coding:utf-8--*--
# Author: Shensg

"""
This's delete NSQ topic and channel!!!!
"""

import re
import requests
import time
from requests.auth import HTTPBasicAuth

# Obtain nsq version
def getNsqVersion(addr):
    r = requests.get(addr, auth=HTTPBasicAuth(username, password))
    # print(r.text)
    s = re.findall('(\s.*[a-z].+?\sVERSION.*)', r.text)
    s = str(s)
    v = re.split(r'[=\'\"]', s)
    # print(v[3])
    return v[3]

# Obtain nsq all topic
def delUnusedTopicAndChannel(addr):
    version = getNsqVersion(addr)
    r = re.split('[.]', version)
    v = int(r[1])
    f = requests.get(addr + "/api/topics", auth=HTTPBasicAuth(username, password))
    f = f.json()
    # print("All topic")
    # print(f)
    topicList = f.get("topics", None)
    for topic in topicList:
        time.sleep(0.01)
        r = requests.get(addr + "/api/topics/" + topic, auth=HTTPBasicAuth(username, password))
        # r = requests.request("GET", addr + "/" + "production.live_event_push")
        data = r.json()
        #print(data)
        l = data.get("nodes", None)[0]
        if len(l.get("channels", None)):
            # Delete unused channel
            res = l.get("channels", None)
            if v == 1:
                print("NSQ greater than or equal to 1.1.0, Is the current version：", version)
                for i in res:
                    if not i.get("clients"):
                        print("Delete unused channel", i.get("topic_name", None), i.get("channel_name", None))
                        r1 = requests.delete(addr + "/api/topics/" + i.get("topic_name", None) + "/" + i.get("channel_name", None), auth=HTTPBasicAuth(username, password))
                        print(r1)
                        time.sleep(0.1)
            elif v == 2:
                print("NSQ version greater than or equal to, Is the current version：", version)
                for i in res:
                    if i.get("client_count") == 0:
                        print("delete unused channel", i.get("topic_name", None), i.get("channel_name", None))
                        r1 = requests.delete(addr + "/api/topics/" + i.get("topic_name", None) + "/" + i.get("channel_name", None), auth=HTTPBasicAuth(username, password))
                        print(r1)
                        time.sleep(0.1)
        else:
            # Delete unused topic
            print("Delete unused topic", l.get("topic_name", None))
            r1 = requests.delete(addr + "/api/topics/" + l.get("topic_name", None), auth=HTTPBasicAuth(username, password))
            print(r1)
            time.sleep(0.1)

if __name__ == "__main__":
    # NSQ username password authentication
    username = ""
    password = ""
    # The corresponding NSQ address needs to be replaced. Please do not add it after the address "/"
    addr = "https://doamin"
    delUnusedTopicAndChannel(addr)
    delUnusedTopicAndChannel(addr)
