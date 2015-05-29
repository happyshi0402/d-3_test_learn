# encoding: utf-8
#!/usr/bin/env python

import MySQLdb
import logging
import time
import threading
import sys
import os

__author__ = 'fuze'

"""
Usage:
    from Mysql_db import DB
     db = DB()
     db.execute(sql)
     db.fetchone()
     db.fetchall()
     :return same as MySQLdb
"""
current_filename = sys.argv[0][sys.argv[0].rfind(os.sep)+1:sys.argv[0].rfind(os.extsep)]
logging.basicConfig(filename=current_filename+'_DB.log', filemode='w')


class DB(object):
    conn = None
    cursor = None

    def connect(self):
        logging.info(time.ctime() + " : connect to mysql server..")
        self.conn = MySQLdb.connect(host='112.124.13.146', port=3306, user='gpo',
                                    passwd='btlc123', db='clinic', charset='utf8')
        # self.conn = MySQLdb.connect(host='localhost', port=3306, user='root',
        #                             passwd='root1256', db='clinic', charset='utf8')

        # self.conn = MySQLdb.connect(host='192.168.120.111', port=3306, user='admin',
        #                             passwd='admin', db='clinic', charset='utf8')

        self.conn.autocommit(True)

    # 线程函数
    def thread(self):
        t = threading.Thread(target=self.conn.ping, args=())
        t.setDaemon(True)
        t.start()
        t.join(2)
        if t.isAlive():
            return 0
        else:
            return 1

    def execute(self, sql_query):
        try:
            logging.info(time.ctime() + " : " + sql_query)
            # 重启超过五次则不再重启
            i = 0
            while i < 3 and self.thread() != 1:
                self.close()
                self.connect()
                self.cursor = self.conn.cursor()
                i += 1
            if i == 3:
                return logging.error(time.ctime() + "execute failed")
            handled_item = self.cursor.execute(sql_query)
        except Exception, e:
            logging.error(e.args)
            logging.info("Reconnecting..")
            self.connect()
            self.cursor = self.conn.cursor()
            logging.info(time.ctime() + " : " + sql_query)
            handled_item = self.cursor.execute(sql_query)
        return handled_item

    def fetchone(self):
        try:
            logging.info(time.ctime() + " : fetchone")
            one_item = self.cursor.fetchone()
        except Exception, e:
            logging.error(e.args)
            logging.info(time.ctime() + " : fetchone failed, return ()")
            one_item = ()
        return one_item

    def fetchall(self):
        try:
            logging.info(time.ctime() + " : fetchall")
            all_item = self.cursor.fetchall()
        except Exception, e:
            logging.error(e.args)
            logging.info(time.ctime() + " : fetchall failed, return ()")
            all_item = ()
        return all_item

    def close(self):
        logging.info(time.ctime() + " : close connect")
        if self.cursor:
            self.cursor.close()
        self.conn.close()
