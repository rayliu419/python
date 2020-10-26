# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import sys


def print_error(item):
    print("marketplace - {}".format(item[2].text))
    print("tag - {}".format(item[5].text))
    print("stringSet - {}".format(item[4].text))
    print("sourceText - {}".format(item[1].text))


def print_normal(of, item):
    of.write(item[2].text)
    of.write("|")
    of.write(item[5].text)
    of.write("|")
    of.write(item[4].text)
    of.write("|")
    if item[1].text != None:
        remove_newline = item[1].text.replace("\n", "")
        of.write(remove_newline)
    else:
        of.write("")
    of.write("\n")


if __name__ == "__main__":
    infile = sys.argv[1]
    output_file = sys.argv[2]
    tree = ET.ElementTree()
    tree.parse(infile)
    all_string = tree.findall("string")
    total = 0
    meet = 0
    tag = {}
    of = open(output_file, "w")
    of.write("marketplace|tag|stringSet|sourceText\n")
    for one_string in all_string:
        total += 1
        try:
            if one_string[0].text == "en_US" and not one_string[5].text in tag:
                meet += 1
                tag[one_string[5].text] = 1
                print_normal(of, one_string)
        except TypeError:
            print_error(one_string)
        except UnicodeEncodeError:
            print_error(one_string)
    print("total - {}".format(total))
    print("meet - {}".format(meet))
    of.close()

