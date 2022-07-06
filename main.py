#!/usr/bin/python
# -*- coding:utf-8 -*-
from ast import Try
from email.policy import strict
import json
import pandas as pd
import os
import tablib
import re
import time

def tranform1():
    data = tablib.Dataset()
    data.headers = ['年龄','出生年','出生地','身份证号','民族','籍贯','姓名','性别']
    with open('./person_info.json', 'r', encoding='utf-8') as f:
        while True:
            linedata = f.readline()
            if not linedata:break
            try:
                row = json.loads(linedata,strict=False)
                body = []
                for k, v in row.items():
                    if k == '_source':
                        for itk,itv in v.items():
                            body.append(itv)
                data.append(tuple(body))
            except:
                continue
            
        f.close()
    with open('./testing.xlsx', 'wb') as f:
        f.write(data.export('xlsx'))
        f.close()

def conver(str):
    # p1 = re.compile("[\u4e00-\u9fa5]\"[\u4e00-\u9fa5]+") #汉字之间引号
    # p2 = re.compile("[[0-9]]\"[\u4e00-\u9fa5]+") # 数字 + " + 汉字
    # p3 = re.compile("\)\"[\u4e00-\u9fa5]+") # ) + " + 汉字
    # p4 = re.compile("[\u4e00-\u9fa5]\"\(+") # 汉字+" + （
    p5 = re.compile("[0-9]\:[0-9]+") #。+"+ 汉字
    p6 = re.compile("[(a-z)(A-Z)(0-9)(\u4e00-\u9fa5) \u8fc7 （ \(   。：，、][ \"]  +[、 ，（。： \((\u4e00-\u9fa5 )(0-9)(a-z)(A-Z)]") #。 汉字 : 汉字
    p7 = re.compile("[(\u4e00-\u9fa5) （ \(   。：，][ \":,  ]+[ ，（。： \((\u4e00-\u9fa5 )]") #。 汉字 : 汉字
    def func(m):
        return m.group().replace("\"","“").replace(":","：").replace(",","，")
    # while True:
    #     m1 = p1.search(str)
    #     if not m1 : break
    #     str = p1.sub(func,str)
    # while True:
    #     m1 = p2.search(str)
    #     if not m1 : break
    #     str = p2.sub(func,str)
    # while True:
    #     m1 = p3.search(str)
    #     if not m1 : break
    #     str = p3.sub(func,str)
    # while True:
    #     m1 = p4.search(str)
    #     if not m1 : break
    #     str = p4.sub(func,str)
    # while True:
    #     m1 = p5.search(str)
    #     if not m1 : break
    #     str = p5.sub(func,str)

    temp = 0
    while True:
        m1 = p5.search(str)
        temp = temp + 1
        if temp > 200:break 
        if not m1 : break
        str = p5.sub(func,str)
    temp = 0
    while True:
        m1 = p6.search(str)
        temp = temp + 1
        if temp > 200:break 
        if not m1 : break
        str = p6.sub(func,str)
    temp = 0
    while True:
        m1 = p7.search(str)
        temp = temp + 1
        if temp > 200:break
        if not m1 : break
        str = p7.sub(func,str)
    return str

if __name__ == '__main__':
    index= 0
    index1= 0
    data = tablib.Dataset()
    data.headers = ['案件详情','案件地址','所属','案件号','城市','案件名']

    with open('./case_data_index.json', 'r', encoding='utf-8') as f:

        data = tablib.Dataset()
        data.headers = ['案件详情','案件地址','所属','案件号','城市','案件名']
        while True:

            linedata = f.readline()
            if not linedata:break
            linedata = linedata.replace("\"{\"CASE\"","{\"CASE\"").replace("\"}\",\"ADDR","\"},\"ADDR")
            linedata = linedata.replace("\"{\"case_state\"","{\"case_state\"")
            linedata = linedata.replace("\"{\"policeJson\"","{\"policeJson\"")
            linedata = linedata.replace("\"{\"reporterJson\"","{\"reporterJson\"")
            linedata = linedata.replace("\"{\"police\"","{\"police\"")
            linedata = linedata.replace("\"{\"caseState\"","{\"caseState\"")
            linedata = linedata.replace("\"{\"reporter\"","{\"reporter\"")
            linedata = linedata.replace("\"{\"suspect\"","{\"suspect\"")
            linedata = linedata.replace("\"110\"","110") #去除110引号
            #去除汉字中间的引号
            linedata = conver(linedata)
            # linedata = linedata.replace()
            try:
                row = json.loads(linedata,strict=False)
                index=index + 1
                index1=index1 + 1
                if index1 >= 10000:
                    with open("./case%s.xlsx"%index, 'wb') as outf:
                        outf.write(data.export('xlsx'))
                        outf.close()
                    data = tablib.Dataset()
                    data.headers = ['案件详情','案件地址','所属','案件号','城市','案件名']
                    index1 = 0
    # data.headers = ['案件详情','案件地址','所属','案件号','城市','案件名']
                body = ["","","","","",""]
                for k, v in row.items():
                    if k == '_source':
                        for sk,sv in v.items():
                            if(sk == 'ADDR_DETL'):
                                for k1,v1 in sv.items():
                                    if(k1 == 'CASE'):
                                        for caseK,caseV in v1.items(): 
                                            if(caseK == 'BRIEF_CASE'):
                                                body[0] = caseV
                            if(sk == 'STD_ADDRESS'):
                                body[1] = sv        
                            if(sk == 'CASE_NUMBER'):
                                body[3] = sv

                            if(sk == 'CASE_NAME'):
                                body[5] = sv

                data.append(tuple(body))

            except:
                print(linedata)

    

    # with open('./case.xlsx', 'wb') as outf:
    
    #     outf.write(data.export('xlsx'))
    #     outf.close()
        # body = []
        # for k, v in row.items():
        #     if k == '_source':
        #         for itk,itv in v.items():
        #             body.append(itv)
        # data.append(tuple(body))
            