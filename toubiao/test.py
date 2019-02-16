#coding:utf-8
import time
import os
cwdpath = os.path.dirname(__file__)

def analyse_file(file):
    print file+' processing...'
    tmpfile = open(file,'w')
    tmpfile.close()

def do_some_code():
    walkfiles = os.walk(cwdpath)

    walk = [x for x in walkfiles]
    filenames = walk[0][2]
    filenames.remove('test.py')

    if filenames:
        dirname = os.path.join(walk[0][0],'result')

        if os.path.isdir(dirname):
            pass
        else:
            print 'mkdir result'
            os.mkdir(dirname)

        listresultfilenames = [os.path.join(dirname,'_'.join(x.split('.'))) for x in filenames]

        for i in listresultfilenames:
            tmpfn = i +' .txt'
            if os.path.isfile(tmpfn):continue

            analyse_file(tmpfn)


if __name__ == '__main__':

    while True:
        do_some_code()
        time.sleep(2)
