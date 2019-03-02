# -*- coding: UTF-8 -*-
import tkinter as tk
import collections
from tkinter import filedialog
import test
import ccat
import copy
import io
import pandas as pd
from pandas import DataFrame as df
currentDict = {}

def hit_me():
    file_type = var.get()
    filepath = pathopen.get()
    if not len(filepath):
        showContentToText(('请选择文件',{}))
        return
    if not file_type.count('.')==1:
        showContentToText(('请选择正确的文件类型',{}))
        return
    if file_type=='.xsh':
        try:
            showContentToText(test.analyse_Xshell_file(filepath))
        except:
            showContentToText(('请选择正确的参数',{}))
        return
    if file_type=='.exe':
        try:
            showContentToText(test.analyseExeByWin32api(filepath))
        except:
            showContentToText(('请选择正确的参数', {}))
        return
    if file_type=='.xml':
        try:
            showContentToText(test.XML2jsonAndDict(filepath))
        except:
            showContentToText(('请选择正确的参数', {}))
        return
    if file_type=='.sqlite':
        try:
            showContentToText(test.analyse_sqlite(filepath))
        except:
            showContentToText(('请选择正确的参数', {}))
        return
    if file_type=='.secureCRT':
        try:
            showContentToText(test.analyse_secureCRT_file(filepath))
        except:
            showContentToText(('请选择正确的参数', {}))
        return
    if file_type == '.evtx':
        try:
            showContentToText(test.analyse_Evtx(filepath))
        except:
            showContentToText(('请选择正确的参数', {}))
        return
    if file_type == '.juniper':
        try:
            showContentToText(test.analyse_JuniperConfig(filepath))
        except:
            showContentToText(('请选择正确的参数', {}))
        return
    if file_type == '.cisco':
        try:
            showContentToText(ccat.parse_cisco(filepath))
        except:
            showContentToText(('请选择正确的参数', {}))
        return

def deletecontent():
    showtext.delete('1.0', tk.END)
    global currentDict
    currentDict.clear()

def showContentToText(Content):
    showtext.delete('1.0',tk.END)
    showtext.insert(tk.INSERT, Content[0])
    global currentDict
    currentDict = copy.deepcopy(Content[1])

def showselectkeyToText(Content):
    selectkeyshowtexxt.delete('1.0',tk.END)
    selectkeyshowtexxt.insert(tk.INSERT, Content)

def selectkey_func():
    _select_key = selectkey.get()
    if len(_select_key) and len(currentDict):
        resultkv = find_key_in_Dict(_select_key,currentDict,[])
        if resultkv:
            showselectkeyToText('['+'->'.join([str(i) for i in resultkv[0]])+'] : ['+str(resultkv[1])+']')
        else:
            showselectkeyToText('not found')
    else:
        selectkeyshowtexxt.delete('1.0', tk.END)

def selectopenPath():
    path_ = filedialog.askopenfilename()
    pathopen.set(path_)

def selectsavePath():
    path_ = filedialog.asksaveasfilename()
    pathsave.set(path_)

def clicksavefile():
    try:
        universeSaveFile(pathsave.get(),showtext.get('0.0',tk.END))
    except:
        pass

def universeSaveFile(filepath,jobj):
    with io.open(filepath,'w',encoding='utf-8') as f:
        f.write(jobj)

def find_key_in_Dict(key,curdict,keys):

    for k,v in curdict.items():
        if key==k:
            keys.append(k)
            return keys,v
        else:
            if type(v)==dict or type(v)==collections.OrderedDict:

                tmpkeys = copy.deepcopy(keys)
                tmpkeys.append(k)
                ret = find_key_in_Dict(key,v,tmpkeys)
                if ret is not None:return ret
    return None

window = tk.Tk()
window.title('文件解析')
window.geometry('800x580')
fm1 = tk.Frame(window)
fm2 = tk.Frame(window)
fm3 = tk.Frame(window)
fm4 = tk.Frame(window)
fm5 = tk.Frame(window)
fm6 = tk.Frame(window)


var = tk.StringVar()
def print_selection():
    pass
r1 = tk.Radiobutton(fm2, text='Xshell',variable=var, value='.xsh',command=print_selection).pack(side=tk.LEFT)
r2 = tk.Radiobutton(fm2, text='.exe',variable=var, value='.exe',command=print_selection).pack(side=tk.LEFT)
r3 = tk.Radiobutton(fm2, text='xml',variable=var, value='.xml',command=print_selection).pack(side=tk.LEFT)
r4 = tk.Radiobutton(fm2, text='sqlite',variable=var, value='.sqlite',command=print_selection).pack(side=tk.LEFT)
r5 = tk.Radiobutton(fm2, text='secureCRT',variable=var, value='.secureCRT',command=print_selection).pack(side=tk.LEFT)
r6 = tk.Radiobutton(fm2, text='evtx',variable=var, value='.evtx',command=print_selection).pack(side=tk.LEFT)
r7 = tk.Radiobutton(fm2, text='juniper',variable=var, value='.juniper',command=print_selection).pack(side=tk.LEFT)
r8 = tk.Radiobutton(fm2, text='cisco',variable=var, value='.cisco',command=print_selection).pack(side=tk.LEFT)

showtext = tk.Text(window)
selectkeyshowtexxt = tk.Text(window,width=50,height=3)

pathopen = tk.StringVar()
pathsave = tk.StringVar()

pathlabel = tk.Label(fm1,text = "需要被解析的文件").pack(side=tk.LEFT)
pathEntry = tk.Entry(fm1, textvariable = pathopen).pack(side=tk.LEFT)
pathButton = tk.Button(fm1, text = "路径选择", command = selectopenPath).pack(side=tk.LEFT)

Analyse_btn = tk.Button(fm3,text='开始解析',command = hit_me).pack(side=tk.LEFT)
deletebtn = tk.Button(fm3, text = "清除内容", command = deletecontent).pack(side=tk.LEFT)

selectkey = tk.StringVar()
selectkeylabel = tk.Label(fm4,text = "填写需要提取的key值").pack(side=tk.LEFT)
selectkeyEntry = tk.Entry(fm4, textvariable = selectkey).pack(side=tk.LEFT)
selectkeyButton = tk.Button(fm4, text = "提取value", command = selectkey_func).pack(side=tk.LEFT)


savelabel = tk.Label(fm5,text = "将解析结果保存").pack(side=tk.LEFT)
saveEntry = tk.Entry(fm5, textvariable = pathsave).pack(side=tk.LEFT)
saveButton = tk.Button(fm5, text = "选择保存路径", command = selectsavePath).pack(side=tk.LEFT)
clicksaveButton = tk.Button(fm5, text = "点击保存", command = clicksavefile).pack(side=tk.LEFT)

pathsavecsv = tk.StringVar()

def selectsavecsvPath():
    path_ = filedialog.asksaveasfilename()
    pathsavecsv.set(path_)

def clicksavecsvfile():
    # universeSaveFile(pathsavecsv.get(), showtext.get('0.0', tk.END))
    try:
        if currentDict:
            curdf = pd.DataFrame(currentDict,index=[0])
            curdf.to_csv(pathsavecsv.get())
    except:
        pass

savecsvlabel = tk.Label(fm6,text = "将解析结果保存为表格形式").pack(side=tk.LEFT)
savecsvEntry = tk.Entry(fm6, textvariable = pathsavecsv).pack(side=tk.LEFT)
savecsvButton = tk.Button(fm6, text = "选择保存路径", command = selectsavecsvPath).pack(side=tk.LEFT)
clicksavecsvButton = tk.Button(fm6, text = "点击保存", command = clicksavecsvfile).pack(side=tk.LEFT)



fm1.pack()
fm2.pack()
fm3.pack()
showtext.pack()
fm4.pack()
selectkeyshowtexxt.pack()
fm5.pack()
fm6.pack()

if __name__ == '__main__':

    # x = 'd'
    # print(str(x))
    window.mainloop()
    #
    # m = collections.OrderedDict()
    # m['i'] = 565
    # m['j'] = collections.OrderedDict({'k':8,'l':98})
    #
    # x = {'a':1,'b':'3','c':{'d':45,'e':{'f':565,'g':'order','h':m}}}
    #
    # print(find_key_in_Dict('k',x,[]))

