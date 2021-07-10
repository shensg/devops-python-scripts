#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Shensg
"""
需要先改数据连接配置 db_conf
需要把SQL文件放在与脚本的同级目录
把SQL文件名字传入进来或者手动修改filename变量
"""

import sys
import threading
import time
try:
    import pymysql
except Exception as e:
    print("pip3 install pymysql")
    sys.exit(1)


Usege = """=======================
Command:
    -h | --help     display this help and exit
    python3 thread_running_sql.py  empty/SQL_filename
"""

class MysqlConnect(object):
    """e
    先实例化MySQL连接
    """
    def __init__(self):
        self.db_conf = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'pwd',
            'database': 'dbname',
            'charset': 'utf8'
        }

    def connectdb(self):
        conn = pymysql.connect(**self.db_conf)
        return conn

# thread = threading.Condition()  # 加线程 lock
class Perform(threading.Thread):
    """
    实例化多线程
    """
    def __init__(self, sql):
        super(Perform, self).__init__()
        self.sql = sql

    def run(self):
        # thread.acquire()
        try:
            while True:
                # time.sleep(10)
                connect = MysqlConnect()
                conn = connect.connectdb()
                cursor = conn.cursor()
                cursor.execute(self.sql)
                result = cursor.fetchall()
                conn.commit()
                cursor.close()
                conn.close()
                print(result)
                return

        except EOFError as e:
            print(e)

def getFilesAndRunning(filename):
    """
    统计行数和SQL，SQL文件尽量不要有空行，因为统计行数会把空行也算再里面
    :param filename:
    :return:
    """
    f = open(filename, 'r')
    runlist = []
    line = len(f.readlines())
    for i in range(line):
        parm = "run" + str(i)
        runlist.append(parm)
        # print(runlist)

    f = open(filename, 'r')
    sqllist = []
    for a in f.readlines():
        sqllist.append(a)


    # 这里的循环不影响线程的的执行，每次循环都是独立产生一个线程，循环结束即停止。线程要把流程执行完才停止
    for o in range(line):
        runlist[o] = Perform(sqllist[o])
        runlist[o].start()
        # print("第", e, "主进程开始")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        filename = "update.sql"
    elif len(sys.argv) == 2:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print(Usege)
            sys.exit(0)
        else:
            filename = sys.argv[1]
    while True:
        print("\033[1;35;0m***running program before checking sql...\033[0m")
        # "再次确认是否执行"
        parma = input("please input (yes/no):")
        if parma == "yes":
            getFilesAndRunning(filename)
            break
        else:
            print("checking your sql, please!!!")
            break
