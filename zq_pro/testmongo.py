import pymongo
from pymongo import MongoClient


class xunfengDB:
    dbxunfeng = MongoClient('localhost', 27017).get_database('xunfeng')
    Collection_Config = dbxunfeng.get_collection('Config')
    Collection_Heartbeat = dbxunfeng.get_collection('Heartbeat')
    Collection_History = dbxunfeng.get_collection('History')
    Collection_Info = dbxunfeng.get_collection('Info')
    Collection_Plugin = dbxunfeng.get_collection('Plugin')
    Collection_Result = dbxunfeng.get_collection('Result')
    Collection_Statistics = dbxunfeng.get_collection('Statistics')
    Collection_Task = dbxunfeng.get_collection('Task')
    Collection_Update = dbxunfeng.get_collection('Update')

config = xunfengDB().Collection_Config

dbxunfeng = MongoClient('localhost', 27017).get_database('xunfeng')


Collection_Config = dbxunfeng.get_collection('Config')
Collection_Heartbeat = dbxunfeng.get_collection('Heartbeat')
Collection_History = dbxunfeng.get_collection('History')
Collection_Info = dbxunfeng.get_collection('Info')
Collection_Plugin = dbxunfeng.get_collection('Plugin')
Collection_Result = dbxunfeng.get_collection('Result')
Collection_Statistics = dbxunfeng.get_collection('Statistics')
Collection_Task = dbxunfeng.get_collection('Task')
Collection_Update = dbxunfeng.get_collection('Update')


dbzq = MongoClient('localhost',27017).get_database('zqCollection')
Collection_zqone = dbzq.get_collection('zqone')

