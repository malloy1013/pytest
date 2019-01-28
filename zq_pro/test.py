from testmongo import *
from testdd.testdd import *
import numpy as np
import pandas as pd
#
import threading
import thread
import os
import time

# print config
# print Collection_Heartbeat
# # print xunfengDB.Collection_Task.find()

# X = 'eee'
#
# def inference():
#     """
#     Forward passing the X.
#     :param X: Input.
#     :return: X*W + b.print [x for x in range(10)]
#     """
#     global X
#     X = 'ssss'
#     print X
#
# def mmm():
#     print X
# # print [x for x in range(10)]
# inference()
# mmm()
# x = np.arange(15).reshape((3,5))
# y = np.arange(15,27)
# b = x
# x[0,:3] = -1
# print x,'\n',b
# print np.array_split(x,4,axis=1)
# print np.vstack((x,y))
# print np.shape(x)
# print np.shape(y)

# x = pd.Series([1,2,3,5,np.nan,np.zeros(8),'34'],[np.nan,'2',3,5,7,8,12])
# print x
# y = pd.DataFrame([1,2,3,5,np.nan,np.zeros(8),'34'])
# print y
# dates = np.arange(6).reshape((2,3))
# df = pd.DataFrame(np.arange(12).reshape((3,4)))

# x = '.'
# a = ['a','2','4er4']
# print ".".join(a)
# print df.iloc[0,2]
# x = np.zeros([1,3])

# print x
# print os.getcwd()

# print get_this_file_parent_path(__file__)

def write_in():
    one = 1
    two = 2
    while True:

        x = {
            'flag':'test',
            '1':one,
            '2':two
        }

        res = Collection_zqone.insert_one(x)

        # print res,'\n'

        one += 1
        two += 2
        time.sleep(4)


def read_out():
    while True:

        res= Collection_zqone.find({'flag':'test'})

        a = [m for m in res]
        for i in a:
            print a
        print Collection_zqone.count({})
        time.sleep(2)
def test():
    while True:
        print 1,'\n'

        time.sleep(1)
if __name__ == '__main__':
    # thread.start_new_thread(write_in,())
    # thread.start_new_thread(read_out,())
    # res = Collection_zqone.insert_one({'one':1,'two':2})
    # print res
    # while True:
    #
    #     time.sleep(5)
    # print Collection_Plugin.find().count()
    print Collection_Plugin.update_many({"count":1},{"$set":{"count":0}})