#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Time:2020-10
# Author:Shensg

import sys
import os
import time
# import readline
import requests


# Gets the current script directory as the working directory // 获取当前脚本目录作为工作目录
dir = sys.path[0]
os.chdir(dir)

# help // 运行脚本的帮助
def used_Usge():
    help = "Example:\npython3 + %s + servername" % (sys.argv[0])
    return help

# obtain current version //获取当前版本
def current_version(sname):
    os.system("docker ps -a | grep -i %s | awk '{print $2}' | awk -F[:] '{print $2}' > ./version.txt" % (sname))
    f = open("./version.txt")
    vold = f.readline()
    return vold

# obtain docker image new version //获取docker最新镜像版本
def obtain_new_version(sname):
    try:
        if sname == 0:
            print("\033[1;31mInsert server name error\033[0m\033[5;32m!!!...\033[0m")
        else:
            r = requests.get("http://stry.snwit.com:5000/v2/%s/tags/list" % (sname))
            i = r.json()
            v = i['tags']
            v.sort(reverse=True)
            # print(v)
            l = v[0]
            # print(l)
            return l
    except EOFError:
        print("\033[1;31mAll version obtain fail, exit\033[0m\033[5;32m!!!...\033[0m")
        sys.exit(3551)

# check versioin update // 检查版本更新
def checkup(sname):
    newv = obtain_new_version(sname)
    # print(newv)
    oldv = current_version(sname)
    # print("this: %s" % (oldv))
    time.sleep(5)
    if newv in oldv:
        print("\033[1;32mThis's the latest version\033[0m\033[5;32m...\033[0m")
        s = "off"
        return s
    else:
        print("\033[1;32mCheck the new version, updating, please wait\033[0m\033[5;32m!!!...\033[0m")
        s = "on"
        print(s)
        return s


# check start running status // 检查启动运行状态
def running_stated(sname):
    os.system("docker ps -a | grep %s | awk '{print $NF}' > ./status.txt" % (sname))
    f1 = open("./status.txt")
    status1 = f1.readline()
    # print("这是状态：%s" % (status1))
    if 'snwit' in status1:
        os.system("docker logs %s | grep -i 'error' > ./out.txt || echo 'on' > ./out.txt" % (sname))
        f2 = open("./out.txt")
        logout = f2.readline()
        # print(logout)
        if 'on' in logout:
            print("\033[1;33m %s server is running success\033[0m\033[5;32m!!!...\033[0m" % (sname))
            s = "on"
            return s
        else:
            print("\033[1;31m %s server is running fail\033[0m\033[5;32m!!!...\033[0m" % (sname))
            s = "off"
            return s
    else:
        print("\033[1;31m%s server is stop\033[0m\033[5;32m!!!...\033[0m")
        s = "no"
        return s

# start server // 启动服务
def start_server(sname):
    while True:
        os.system("docker ps -a |grep %s | awk '{print $NF}' > ./status.txt" % (sname))
        f = open("./status.txt")
        status = f.readline()
        if sname in status:
            print("\033[1;32m%s server is running...\nstopping, please wait!\033[0m\033[5;32m...\033[0m" % (sname))
            stop_server(sname)
            os.system("/data/scripts/runserver %s %s" % (sname, obtain_new_version(sname)))
            time.sleep(3)
            s = running_stated(sname)
            if 'on' in s:
                return s
            elif 'no' in s:
                return s

        else:
            os.system("/data/scripts/runserver %s %s" % (sname, obtain_new_version(sname)))
            time.sleep(3)
            s = running_stated(sname)
            if 'on' in s:
                return s
            elif 'no' in s:
                return s

# stop server // 停止服务
def stop_server(sname):
    print("\033[1;32m%s server is stopping\033[0m\033[5;32m...\033[0m" % (sname))
    while True:
        os.system("docker stop %s" % (sname))
        time.sleep(3)
        os.system("docker rm %s" % (sname))
        time.sleep(3)
        os.system("docker ps -a | grep %s | awk '{print $NF}' > ./stop.txt" % (sname))
        f = open("./stop.txt")
        stop_out = f.readline()
        if sname in stop_out:
            print("\033[1;31m %s server is running !!! please wait\033[0m\033[5;32m...\033[0m" % (sname))
            time.sleep(2)
            # sys.exit(2)
        else:
            print("\033[1;32m%s server is stop\033[0m\033[5;32m...\033[0m" % (sname))
            time.sleep(2)
            s = "stop"
            return s
            # sys.exit()

# update failed version rollback // 更新失败时版本回滚
def rollback_server(sname):
    print("\033[1;33m%s update fail, %s server is rollback !!!\033[0m\033[5;32m...\033[0m" % (sname, sname))
    f = open("./version.txt")
    vold = f.readline()
    while True:
        stop_server(sname)
        os.system("/data/scripts/runserver %s %s" % (sname, vold))
        time.sleep(3)
        s = running_stated(sname)
        if 'on' in s:
            sys.exit()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        h = used_Usge()
        print(h)
    else:
        sname = sys.argv[1]
        obtain_new_version(sname)
        l = checkup(sname)
        if 'on' in l:
            l1 = start_server(sname)
            if 'no' in l1:
                while True:
                    rollback_server(sname)
