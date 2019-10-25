# -*- coding: utf-8 -*-

import datetime, calendar
import time
# 获取的为当前系统时间
date = datetime.datetime.now()

# 返回昨天日期
def getYesterday():
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    yesterday=today-oneday
    return yesterday

# 返回今天日期
def getToday():
    return datetime.date.today()

# 获取给定参数的前几天的日期，返回一个list
def getDaysByNum(num):
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    li=[]
    for i in range(0,num):
        #今天减一天，一天一天减
        today=today-oneday
        #把日期转换成字符串
        #result=datetostr(today)
        li.append(datetostr(today))
    return li

# 将字符串转换成datetime类型
def strtodatetime(datestr,format):
    return datetime.datetime.strptime(datestr,format)

# 时间转换成字符串,格式为2008-08-02
def datetostr(date):
    return  str(date)[0:10]

# 两个日期相隔多少天，例：2008-10-03和2008-10-01是相隔两天
def datediff(beginDate,endDate):
    format="%Y-%m-%d";
    bd=strtodatetime(beginDate,format)
    ed=strtodatetime(endDate,format)
    oneday=datetime.timedelta(days=1)
    count=0
    while bd!=ed:
        ed=ed-oneday
        count+=1
    return count

# 获取两个时间段的所有时间,返回list
def getDays(beginDate,endDate):
    format="%Y-%m-%d";
    bd=strtodatetime(beginDate,format)
    ed=strtodatetime(endDate,format)
    oneday=datetime.timedelta(days=1)
    num=datediff(beginDate,endDate)+1
    li=[]
    for i in range(0,num):
        li.append(datetostr(ed))
        ed=ed-oneday
    return li

# 获取当前年份 是一个字符串
def getYear():
    return str(datetime.date.today())[0:4]

# 获取当前月份 是一个字符串
def getMonth():
    return str(datetime.date.today())[5:7]

# 获取当前天 是一个字符串
def getDay():
    return str(datetime.date.today())[8:10]
def getNow():
    return datetime.datetime.now()


if __name__ == "__main__":
    print(getYesterday())
    print(getDaysByNum(3))
    print(getDays('2008-10-01','2008-10-05'))

    print(str(getYear())+getMonth()+getDay())
    print(getNow())

    string = time.strftime('%Y-%m-%d',time.localtime())
    print(type(string))

