#coding=utf-8

import re
import string

# python3 is different from python2 in encoding

#############################################################################
#  function list
#############################################################################


def strQ2B(ustring):
    '''
    输入需要是unicode编码！！
    全角转半角
    :param ustring:
    :return:
    '''
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:  #全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
            inside_code -= 65248
        rstring += chr(inside_code)
    return rstring

def strB2Q(ustring):
    '''
    输入需要是unicode编码！！
    半角转全角
    :param ustring:
    :return:
    '''
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 32:   #半角空格直接转化
            inside_code = 12288
        elif inside_code >= 32 and inside_code <= 126:  #半角字符（除空格）根据关系转化
            inside_code += 65248
        rstring += chr(inside_code)
    return rstring

def filter_chars(input_string):
    for x in input_string:
        if (x.decode("utf8") in ["(", "（", ")", "）","", "-"]):
            return False
        return True

def get_content_within_bracket(input_string):
    '''
    只处理半角
    :param input_string:
    :return:
    '''
    regex = re.compile(r"\((.*?)\)")
    temp = re.findall(regex, input_string)
    return temp

def get_rid_of_bracket(input_string):
    '''
    只处理半角
    :param input_string:
    :return:
    '''
    regex = re.compile(r"\(.*?\)")
    temp = re.sub(regex, "", input_string)
    return temp

def filter_string(line):
    '''
    对行做清理，删除[,-,(,)], 括号里的内容等。
    :param line:
    :return:
    '''
    line = strQ2B(line.decode("utf8"))
    line = line.encode("utf8")
    line = get_rid_of_bracket(line)
    line = re.sub("[\-\s+]", "", line)
    return line

def get_rid_of_area_suffix(string):
    '''
    输入需要utf8
    :param string:
    :return:
    '''
    result = ""
    reg = re.compile("")
    if (string.endswith("市")):
        reg = re.compile(r"市$")
    elif (string.endswith("区")):
        reg = re.compile(r"区$")
    elif (string.endswith("县")):
        reg = re.compile(r"县$")
    elif(string.endswith("自治县")):
        reg = re.compile(r"自治县$")
    result = reg.sub("", string)
    if (len(result) / 3 == 1):
        # 去完以后只剩一个字了，有问题
        result = string
    return result

def sort_str_by_length_desc(list):
    sort_list = list
    sort_list.sort(key=len, reverse=True)
    return sort_list

def strip_punctuation(temp):
    '''
    string里面有很多常量存储，可以使用
    :param temp:
    :return:
    '''
    return temp.strip(string.punctuation)

#############################################################################
#  test functions
#############################################################################

def Q2B_B2Q_test():
    b = strQ2B("ｍｎ123abc博客园。")
    print((b.encode("utf8")))
    c = strB2Q("ｍｎ123abc博客园")
    print((c.encode("utf8")))

#############################################################################
#  main function
#############################################################################
    
if __name__ == '__main__':
    Q2B_B2Q_test()
    print((string.punctuation))
    print((strip_punctuation("~!@#:123")))