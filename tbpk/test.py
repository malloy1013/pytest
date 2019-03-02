#coding=utf-8
import time

import sys
import json
import chardet #万能转码
import os
import sqlite3
import rsa
import copy #deepcopy
import mmap
import contextlib
import Evtx
from Evtx.Evtx import FileHeader
from Evtx.Views import evtx_file_xml_view
import io
import pefile
import win32api
import pandas as pd
import numpy as np
import string, shutil,re
import xmltodict
import collections
import datetime
import filetime
from ldif3 import LDIFParser
from pprint import pprint

from juniper_config_parser import JuniperConfig
from ciscoconfparse import CiscoConfParse
cwdpath = os.path.dirname(__file__)

def analyse_cisco():
    pass

def analyse_JuniperConfig(filepath):
    a = JuniperConfig(open(os.path.join(cwdpath, 'juniper_de.txt')))
    jobj = json.dumps(a, ensure_ascii=False, indent=2)
    return jobj,a


def ldifparse(filepath):
    parser = LDIFParser(open(filepath, 'r'))
    parser.parse()

    print(parser.records_read)


def universeSaveFile(filepath,jobj):
    with io.open(filepath,'w',encoding='utf-8') as f:
        f.write(jobj)

def XML2jsonAndDict(filepath):

    with open(filepath,'rb') as f:
        txt = f.read()
    typetxt = chardet.detect(txt)
    xml_str = txt.decode(typetxt['encoding'])
    # 将读取的xml内容转为json
    xmldict = xmltodict.parse(xml_str)

    jobj = json.dumps(xmldict, ensure_ascii=False, indent=2)

    return jobj,xmldict


def analyse_secureCRT_file(filepath):
    resultdict = {}
    with open(filepath,'rb') as f:
        txt = f.read()
    typetxt = chardet.detect(txt)
    txtlines = txt.decode(typetxt['encoding']).splitlines()
    tmpkey = ''
    for m in txtlines:
        if re.search(r'"\? ",0,"\\n"',m):break
        if re.search(r'[A-Z]:"',m) and re.search(r'"=',m):
            a = re.split(r'"=',m)[0]+'\"'
            tmpkey = a
            b = re.split(r'"=',m)[1]

            resultdict[a] = b
        else:
            tmpvalue = resultdict[tmpkey]
            tmpvalue += m
            resultdict [tmpkey] = tmpvalue
    jobj = json.dumps(resultdict, ensure_ascii=False, indent=2)
    return jobj,resultdict

def analyse_Xshell_file(filepath):
    resultdict = {}
    with open(filepath, 'rb') as f:
        txt = f.read()
    typetxt = chardet.detect(txt)
    txtlines = txt.decode(typetxt['encoding']).splitlines()
    tmpkey = ''
    tmpdict = {}
    for m in txtlines:
        if re.match(r'\[.*.*\]',m):
            if len(tmpdict):

                resultdict[copy.deepcopy(tmpkey)] = copy.deepcopy(tmpdict)
                tmpkey = m
                tmpdict.clear()
            else:
                tmpkey = m
        elif re.match(r'.*=.*',m):
            tmpdict[copy.deepcopy(m.split('=')[0])] = copy.deepcopy(m.split('=')[1])

        else:
            pass
    if len(tmpkey):
        resultdict[copy.deepcopy(tmpkey)] = copy.deepcopy(tmpdict)

    jobj = json.dumps(resultdict, ensure_ascii=False, indent=2)
    # resultfilename = os.path.splitext(os.path.split(filepath)[1])[0]
    #
    # with io.open(os.path.join(cwdpath,'result',resultfilename+'.json'),'w',encoding='utf-8') as f:
    #
    #
    #     f.write(jobj)
    return jobj,resultdict

def analyseExeByWin32api(fname):
    """
       读取给定文件的所有属性, 返回一个字典.
       """
    propNames = ('Comments', 'InternalName', 'ProductName',
                 'CompanyName', 'LegalCopyright', 'ProductVersion',
                 'FileDescription', 'LegalTrademarks', 'PrivateBuild',
                 'FileVersion', 'OriginalFilename', 'SpecialBuild')

    props = {'FixedFileInfo': None, 'StringFileInfo': None, 'FileVersion': None}
    strInfo = {}
    try:
        fixedInfo = win32api.GetFileVersionInfo(fname, '\\')
        props['FixedFileInfo'] = fixedInfo
        props['FileVersion'] = "%d.%d.%d.%d" % (fixedInfo['FileVersionMS'] / 65536,
                                                fixedInfo['FileVersionMS'] % 65536, fixedInfo['FileVersionLS'] / 65536,
                                                fixedInfo['FileVersionLS'] % 65536)

        # \VarFileInfo\Translation returns list of available (language, codepage)
        # pairs that can be used to retreive string info. We are using only the first pair.
        lang, codepage = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')[0]

        # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
        # two are language/codepage pair returned from above


        for propName in propNames:
            strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
            ## print str_info
            strInfo[propName] = win32api.GetFileVersionInfo(fname, strInfoPath)

        strInfo['FileVersion']="%d.%d.%d.%d" % (fixedInfo['FileVersionMS'] / 65536,
                                                fixedInfo['FileVersionMS'] % 65536, fixedInfo['FileVersionLS'] / 65536,
                                                fixedInfo['FileVersionLS'] % 65536)
        props['StringFileInfo'] = strInfo
    except Exception as e:
        print(e)

    jobj = json.dumps(strInfo, ensure_ascii=False, indent=2)
    # resultfilename = os.path.splitext(os.path.split(fname)[1])[0]
    # with io.open(os.path.join(cwdpath, 'result', resultfilename + '.json'), 'w', encoding='utf-8') as f:
    #
    #     f.write(jobj)
    return jobj,strInfo



def analyse_exe_dll(exepath):
    pe = pefile.PE(exepath)
    # with open(os.path.join(cwdpath,'result','PEresult.txt'),'w') as f:
    #     f.write(pe)
    print (pe.FILE_HEADER)
    # pe.write(os.path.join(cwdpath,'PEresult.txt'))
    return pe

def analyse_Evtx(EvtxPath):
     # 日志文件的路径
    resultdict = {}
    with open(EvtxPath, 'r') as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as buf:
            fh = FileHeader(buf, 0)
            # 构建一个xml文件，根元素是Events

            # 遍历事件

            try:
                i = 0
                for a, b in evtx_file_xml_view(fh):
                    resultdict[i] = xmltodict.parse(a)
                    i = i + 1
            except Exception as e:
                print(e)

    jobj = json.dumps(resultdict, ensure_ascii=False, indent=2)
    return jobj,resultdict


def OnlyBufferToStr(m):
    if type(m)==bytes:
        typem = chardet.detect(m)
        if typem['encoding']:
            encodeingvalue = ''
            try:
                encodeingvalue = m.decode(typem['encoding'])
            except UnicodeError as e:
                encodeingvalue = '编码格式为: ['+typem['encoding']+'] 的数据'
            finally:
                return encodeingvalue
        else:
            return '无法解析的数据'
    else:
        return m

def analyse_sqlite(file):
    resultdict = {}
    with sqlite3.connect(file) as con:
        # read_sql_query和read_sql都能通过SQL语句从数据库文件中获取数据信息
        dfname = pd.read_sql_query("select name from sqlite_master where type='table' order by name;", con=con)
        # df = pd.read_sql("SELECT * FROM test_table", con=con)

        for i in [v for v in dfname.to_dict()['name'].values()]:
            df = pd.read_sql_query("SELECT * FROM "+i+";", con=con)

            tmpdict = df.transpose().to_dict()


            tmpdict2 = dict(map(lambda k_v:(k_v[0],dict(map(lambda x_y:(x_y[0],OnlyBufferToStr(x_y[1])) ,k_v[1].items()))),tmpdict.items()))

            resultdict[i] = tmpdict2


    # df1 = df.drop(labels='encrypted_value',axis=1)

    jobj = json.dumps(resultdict, ensure_ascii=False, indent=2)
    return jobj,resultdict

def analyse_file(file):
    filestr = ''
    print (file+' processing...')
    if os.path.isfile(file):
        extname = os.path.splitext(file)[1]

        if extname.lower() == '.sqlite' or extname.lower() == '':
            filestr = analyse_sqlite(file)

        elif extname.lower() == '.evtx':
            filestr = analyse_Evtx(file)


    with open(os.path.join(os.path.split(file)[0],'result',os.path.split(file)[-1]),'w') as f:
        f.write(filestr)



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
            print ('mkdir result')
            os.mkdir(dirname)

        # listresultfilenames = [os.path.join(dirname,'_'.join(x.split('.'))) for x in filenames]

        for i in filenames:
            analyse_file(os.path.join(cwdpath,i))

def analyse_ipconfig(filepath):
    with open(filepath, 'rb') as f:
        txt = f.read()
    typetxt = chardet.detect(txt)
    txtlines = txt.decode(typetxt['encoding']).splitlines()
    resultdict = {}
    tmpdict = {}
    tmpkey = ''
    littlekey = ''
    for m in txtlines:
        m = m.strip()
        if m=='':
            continue
        if re.search(r'Windows\sIP',m):#头标题
            tmpkey = m.split(':')[0]
            print (tmpkey)
        elif re.search(r'[\.\s]+:',m):#value内容解析

            a = copy.deepcopy(re.split(r'[\.\s]+:',m)[0])
            b= copy.deepcopy(re.split(r'[\.\s]+:',m)[1])
            # print a,b
            tmpdict[a] = b
            littlekey = copy.deepcopy(a)
        else:
            if re.search(r'^[\u2E80-\u9FFF|a-z|A-Z]+.*:',m):#二级标题解析
                resultdict[copy.deepcopy(tmpkey)] = copy.deepcopy(tmpdict)
                tmpkey = m.split(':')[0]
                # print tmpkey
                tmpdict.clear()
            else:

                tmpstr = tmpdict[littlekey]
                tmp2str = tmpstr+','+m
                tmpdict[littlekey] = tmp2str
    if len(tmpkey):
        resultdict[copy.deepcopy(tmpkey)] = copy.deepcopy(tmpdict)

    jobj = json.dumps(resultdict, ensure_ascii=False, indent=2)
    # resultfilename = os.path.splitext(os.path.split(filepath)[1])[0]
    # with io.open(os.path.join(cwdpath,'result',resultfilename+'.json'),'w',encoding='utf-8') as f:
    #
    #     f.write(jobj)
    print(jobj)
    return jobj,resultdict
    # print jobj
    # print json.dumps(resultdict, encoding="UTF-8", ensure_ascii=False)

def ie_cookies(filepath):
    with open(filepath, 'rb') as f:
        txt = f.read()
    typetxt = chardet.detect(txt)
    txtlines = txt.decode(typetxt['encoding']).splitlines()
    resultdict = {}
    i = 0
    j = 0
    tmpdict = {}
    for strline in txtlines:
        _str = strline.strip()
        if not len(_str):continue
        if _str=='*':
            resultdict[j] = copy.deepcopy(tmpdict)
            j +=1
            i = 0
            tmpdict.clear()
        elif i==0:
            tmpdict['Cookie变量名'] = _str
            i +=1
        elif i ==1:
            tmpdict['Cookie变量值'] = _str
            i += 1
        elif i ==2:
            tmpdict['该Cookie变量所属域'] = _str
            i += 1
        elif i ==3:
            tmpdict['可选标志'] = _str
            i += 1
        elif i ==4:
            tmpdict['该Cookie过期时间的高位整数'] = _str
            i += 1
        elif i ==5:
            tmpdict['该Cookie过期时间的低位整数'] = _str
            i += 1
        elif i ==6:
            tmpdict['该Cookie创建时间的高位整数'] = _str
            i += 1
        elif i ==7:
            tmpdict['该Cookie创建时间的低位整数'] = _str
            i += 1
    jobj = json.dumps(resultdict, ensure_ascii=False, indent=2)
    return jobj, resultdict

def change_high_low(high,low):
    return ((high >> 32 & 0xffffffff) | (low & 0xffffffff))



if __name__ == '__main__':



    filepath = sys.argv[1]

    type_analyse = sys.argv[2]

    save_filepath = sys.argv[3]


    if type_analyse == '-xsh':
        resulttuple = analyse_Xshell_file(filepath)
        universeSaveFile(save_filepath, resulttuple[0])

    elif type_analyse == '-exe':
        resulttuple = analyseExeByWin32api(filepath)
        universeSaveFile(save_filepath, resulttuple[0])

    elif type_analyse == '-xml':
        resulttuple = XML2jsonAndDict(filepath)
        universeSaveFile(save_filepath, resulttuple[0])

    elif type_analyse == '-sqlite':
        resulttuple = analyse_sqlite(filepath)
        universeSaveFile(save_filepath, resulttuple[0])

    elif type_analyse == '-secureCRT':
        resulttuple = analyse_secureCRT_file(filepath)
        universeSaveFile(save_filepath, resulttuple[0])

    elif type_analyse == '-evtx':
        resulttuple = analyse_Evtx(filepath)
        universeSaveFile(save_filepath, resulttuple[0])

    elif type_analyse == '-juniper':
        resulttuple = analyse_JuniperConfig(filepath)
        universeSaveFile(save_filepath, resulttuple[0])

    else:
        print('参数错误')


    # ldifparse(os.path.join(cwdpath,'cygwin.ldif'))

    # parse = CiscoConfParse('SW.cfg', syntax='ios')
    # unshut_objs = parse.find_objects_wo_child(r'^interface', r'shutdown')
    # parse.ioscfg[:]
    # print(parse.ioscfg[:])


    # a = ciscoconfparse.CiscoConfParse(os.path.join(cwdpath,'lyq','C6509-01.txt'))
    #
    # print(a.ConfigObjs)
    # print(filetime.to_datetime(change_high_low(507234048,30737287)))

    # print(ie_cookies(os.path.join(cwdpath,'ie','0MM7Y132.txt'))[1])
    # m = buffer('ee')
    # x = collections.OrderedDict()
    # print(type(x)==collections.OrderedDict)
    # analyse_secureCRT_file(os.path.join(cwdpath,'39.107.117.89.ini'))
    # analyse_sqlite(os.path.join(cwdpath,'key4.db'))
    # analyse_Evtx(os.path.join(cwdpath,'testqwe.evtx'))
    # analyseExeByWin32api(os.path.join(cwdpath,'pythonw.exe'))
    # analyse_Xshell_file(os.path.join(cwdpath,'e.xsh'))
    # analyse_ipconfig(os.path.join(cwdpath,'ipconfig_displaydns.txt'))
    # print re.split(r'[\.\s]+:\s','asdfdas. . . : adsfsad')
    # x = analyse_exe_dll(os.path.join(cwdpath,'SetupChipsetx64.msi'))
    # with open(os.path.join(cwdpath,'ipconfig.txt'),'r') as f:
    #     txt = f.read()
    #     type = chardet.detect(txt)
    #     print type
    # a = {'a':1,'b':2}
    # print dict(map(lambda (x,y):(x,unicode(y)) ,a.items()))
    # x = analyseExeByWin32api(os.path.join(cwdpath,'SetupChipsetx64.msi'))

    # with open(os.path.join(cwdpath,'SetupChipsetx64.msi'),'rb') as f:
    #     txt = f.read()
    # typetxt = chardet.detect(txt)
    # xml_str = txt.decode(typetxt['encoding'])
    # print(xml_str)