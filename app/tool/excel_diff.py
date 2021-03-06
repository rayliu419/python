# -*- coding: UTF-8 -*-

import csv
import sys
from optparse import OptionParser
import json


def map_keys_to_index(header, key_array):
    index_array = []
    for i, val in enumerate(header):
        if (val in key_array):
            index_array.append(i)
    return index_array


def combine_key(row, index_array):
    key_str_array = []
    for i in index_array:
        key_str_array.append(row[i])
    return "++".join(key_str_array)


def combine_value(ignore_columns, header, row):
    if (len(header) != len(row)):
        print("length of header is not equal length of row!")
        sys.exit(-1)
    value_map = dict()
    i = 0
    while (i < len(header)):
        if (header[i] not in ignore_columns):
            # omit the ignore column
            value_map[header[i]] = row[i]
    return value_map


def transfer_row_to_record(ignore_columns, header, row, index_array, record_set):
    key = combine_key(row, index_array)
    if (key in record_set):
        print("duplicate key record")
        sys.exit(-1)
    value = combine_value(ignore_columns, header, row)
    record_set[key] = value


def parse_file_to_record(file, key_array, ignore_columns, record_set):
    with open(file, 'rb') as csvfile1:
        reader = csv.reader(csvfile1, delimiter=' ', quotechar='|')
        # first row is column name
        header = reader[0]
        if (len(header) > set(header)):
            print("duplicate column name!")
            sys.exit(-1)
        index_array = map_keys_to_index(header, key_array)
        for row in reader[1:]:
            transfer_row_to_record(ignore_columns, header, row, index_array, record_set)
        return header

def header_check(header1, header2, ignore_columns):
    header1_left = list(set(header1).difference(set(ignore_columns)))
    header2_left = list(set(header2).difference(set(ignore_columns)))
    header1_left = sorted(header1_left)
    header2_left = sorted(header2_left)
    return cmp(header1_left, header2_left)

def compare_record(key, record_set1, record_set2, diff_result):
    record1 = record_set1[key]
    record2 = record_set2[key]
    put = False
    diff_columns_set = dict()
    for k in record1:
        if (record1[k] != record2[k]):
            temp_arr = []
            temp_arr.append(record1[k])
            temp_arr.append(record2[k])
            diff_columns_set[k] = temp_arr
            put = True
    if (put == True):
        json_str1 = json.dumps(record1[key])
        json_str2 = json.dumps(record2[key])
        json_str3 = json.dumps(diff_columns_set)
        diff_result[key] = [json_str1, json_str2, json_str3]


def print_diff_result(ignore_rows, file1_exclusive, file2_exclusive, diff_result):
    if (ignore_rows != "true"):
        print("file exists only in file1 : \n")
        for i in file1_exclusive:
            print(i)
            print(json.dumps(file1_exclusive[i]))
        print("file exists only in file2 : \n")
        for j in file2_exclusive:
            print(j)
            print(json.dumps(file1_exclusive[j]))
        print('exists in file1 and file2, but not equals: \n')
        for k in diff_result:
            print(k)
            print("in file 1 : ")
            print(diff_result[0])
            print("in file 2 : ")
            print(diff_result[1])
            print("diff columns : ")
            print(diff_result[2])



if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("", "--key", dest="key", help="indicate record key")
    parser.add_option("", "--ignore_columns", dest="ignore_columns", help="indicate ignore_colunms, default is None")
    parser.add_option("", "--ignore_rows", dest="ignore_rows",
                      help="indicate ignore rows, default is display different rows")
    parser.add_option("", "--file1", dest="file1", help="indicate excel file1")
    parser.add_option("", "--file2", dest="file2", help="indicate excel file2")
    (options, args) = parser.parse_args()
    if (options.key == ""):
        print("must indicate a row key!")
        sys.exit(-1)
    key_array = options.key.split(',')
    ignore_columns = options.ignore_columns.split(',')
    index_array1 = []
    index_array2 = []
    record_set1 = dict()
    record_set2 = dict()

    header1 = parse_file_to_record(options.file1, key_array, ignore_columns, record_set1)
    header2 = parse_file_to_record(options.file2, key_array, ignore_columns, record_set2)

    if (header_check(header1, header2, ignore_columns) != 0):
        print("the files contains different columns")
        sys.exit(-1)

    record_key1_set = list(record_set1.keys());
    record_key2_set = list(record_set2.keys());
    union_keys = list(set(record_key1_set).union(set(record_key2_set)))

    file1_exclusive = dict()
    file2_exclusive = dict()
    diff_result = dict()
    for key in union_keys:
        if (key in record_set1) == False:
            file2_exclusive[key] = record_set2[key]
        elif (key in record_set2) == False:
            file1_exclusive[key] = record_set1[key]
        else:
            compare_record(key, record_set1, record_set2, diff_result)
    print_diff_result(options.ignore_rows, file1_exclusive, file2_exclusive, diff_result)