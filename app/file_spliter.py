#-*- coding: UTF-8 -*-

import os
import math
import sys


def split_file_with_equal_line(filename, part):
    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)
    linenum = sum(1 for line in open(filename))
    line_each_file = math.floor(int(linenum) / part) + 1
    split_prefix = basename + "."
    if (dirname != ""):
        split_cmd = "cd %s && split -a 1 -l %d %s %s" % (dirname, int(line_each_file), basename,
                                                     split_prefix)
    else:
        split_cmd = "split -a 1 -l %d %s %s" % (int(line_each_file), basename, split_prefix)
    os.system(split_cmd)
    split_files = []
    for i in range(0, part):
        if (dirname != ""):
            split_files.append(dirname + "/" + split_prefix + chr(97 + i))
        else:
            split_files.append(split_prefix + chr(97 + i))
    return split_files

# usage: python file_spliter.py file
if __name__ == '__main__':
    info = split_file_with_equal_line(sys.argv[1], 2)
    print(info)
