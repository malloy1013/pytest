# -*- coding: UTF-8 -*-
from pymongo import MongoClient
import Config

# 数据库连接
class MongoDB(object):
    def __init__(self, host=Config.ProductionConfig.DB, port=Config.ProductionConfig.PORT, database=Config.ProductionConfig.DBNAME, username='', password=''):
        self.host = host
        self.port = port
        self.database = database
        self.conn = MongoClient(self.host, self.port)
        self.coll = self.conn[self.database]
        # self.coll.authenticate(username, password)
