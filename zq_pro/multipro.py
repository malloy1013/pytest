from multiprocessing import Process,Queue,Pool
import os,time,random
def test_fun(name):
    print 'this is '+name+str(os.getpid())

def task_fun(name):
    print 'Now run task:'+str(name)
    start_time = time.time()
    time.sleep(random.random()*3)
    end_time = time.time()
    print 'task:'+str(name)+'run '+str(end_time-start_time)

if __name__ == '__main__':
    print('Parent process %s.' % os.getpid())
    # p = Process(target=test_fun,args={'test'})
    # p.start()
    # p.join()
    # print 'all ends'
    p = Pool(4)
    for i in range(5):
        p.apply_async(task_fun,args=[i])
    print 'subprocesses will start!'
    p.close()
    p.join()
    print 'all ends'

#
# def long_time_task(name):
#     print('Run task %s (%s)...' % (name, os.getpid()))
#     start = time.time()
#     time.sleep(random.random() * 3)
#     end = time.time()
#     print('Task %s runs %0.2f seconds.' % (name, (end - start)))
#
# if __name__=='__main__':
#     print('Parent process %s.' % os.getpid())
#     p = Pool(4)
#     for i in range(5):
#         p.apply_async(long_time_task, args=(i,))
#     print('Waiting for all subprocesses done...')
#     p.close()
#     p.join()
#     print('All subprocesses done.')