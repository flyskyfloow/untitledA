#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql


class MyMysql:
    """
    数据库相关操作
    """
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        """
        得到连接返回连接信息
        charset = 'utf8' 需要设置否则入库可能会报错 
        返回：cursor 
        :return: 
        """
        if not self.db:
            raise (NameError, "没有设置数据参数")
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset='utf8')
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "数据库连接失败！请检查参数")
        else:
            return cur

    def ExecQuery(self, sqle):
        """
        执行 查询语句
        :param sql: 
        :return: 
        """
        cur = self.__GetConnect()
        cur.execute(sqle)
        resList = cur.fetchall()
        self.conn.close()
        return resList

    def ExecNonQuery(self, sql):
        """
        执行库建表
        :param dbname: 
        :param sql: 
        :return: 
        """
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        # 在scrapy中使用 这个模块关闭下面一句话，因为 scrapy的 pipeline 中的 close_spider关闭数据连接
        # 可以减少数据的重连次数
        # self.conn.close()
        print(sql)


if __name__ == "__main__":
    sql = "select version();"
    mysqlQuery = MyMysql("192.168.1.158", "root", "123456", "ssrnDB")
    # mysqlQuery.ExecNonQuery(sql)
    print(mysqlQuery.ExecQuery(sql))
