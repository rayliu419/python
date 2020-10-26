from optparse import OptionParser
from operator import itemgetter

delimiter="___"
line_num=0
comments_empty_num=0


def find_indexes_in_list(names, full_names):
    index = []
    for name in names:
        for i in range(0, len(full_names)):
            if (full_names[i] == name):
                index.append(i)
    return index


def to_tuple(a):
    x = a
    if type(a) != tuple:
        x = tuple(a)
    if type(a) == str:
        x = (a,)
    return x

def parse_indexes(line, options):
    linesplit = line.strip().split("\t")
    rowKey_name = options.rowKeys.strip().split(",")
    reserved_column_name = options.reserved.strip().split(",")
    distribution_column_name = options.column.strip().split(",")
    rowKey_index = find_indexes_in_list(rowKey_name, linesplit)
    reserved_index = find_indexes_in_list(reserved_column_name, linesplit)
    column_index = find_indexes_in_list(distribution_column_name, linesplit)
    return rowKey_index, reserved_index, column_index


def store_info(compute_dict, rowKey_values, reserved_values, column_values, options):
    global delimiter
    key = delimiter.join(rowKey_values)
    distribution_column_name = options.column.strip().split(",")
    if key in compute_dict:
        for name, value in zip(distribution_column_name, column_values):
            if name in compute_dict[key]:
                if value in compute_dict[key][name]:
                    compute_dict[key][name][value] += 1
                else:
                    compute_dict[key][name][value] = 1
            else:
                compute_dict[key][name] = dict()
                compute_dict[key][name][value] = 1
    else:
        compute_dict[key] = dict()
        compute_dict[key]["reserved_values"] = reserved_values
        for name, value in zip(distribution_column_name, column_values):
            compute_dict[key][name] = dict()
            compute_dict[key][name][value] = 1


def handle_file(file, options):
    global line_num
    global comments_empty_num
    reserved_index = []
    rowKey_index = []
    column_index = []
    compute_dict = dict()
    with open(file) as infile:
        for line in infile:
            line_num += 1
            if (line_num == 1):
                rowKey_index, reserved_index, column_index = parse_indexes(line, options);
            else:
                line = line.replace("\r\n", "")
                linesplit = line.strip().split("\t")
                if len(linesplit) == 12:
                    linesplit.append("empty")
                    comments_empty_num += 1
                rowKey_values = itemgetter(*rowKey_index)(linesplit)
                reserved_values = itemgetter(*reserved_index)(linesplit)
                column_values = itemgetter(*column_index)(linesplit)
                rowKey_values = to_tuple(rowKey_values)
                reserved_values = to_tuple(reserved_values)
                column_values = to_tuple(column_values)
                store_info(compute_dict, rowKey_values, reserved_values, column_values, options)
    compute_distribution(options, compute_dict)


def compute_distribution(options, compute_dict):
    global delimiter
    output_file = options.file + ".distribution.txt"
    of = open(output_file, "w")
    for k, v in compute_dict.iteritems():
        of.write("\n")
        key_content = []
        reserved_content = []
        name2value_and_count = dict()
        key_content = k.split(delimiter)
        for k2, v2 in v.iteritems():
            if k2 == "reserved_values":
                reserved_content = v2
            else:
                name2value_and_count[k2] = v2
        rowKey_name = options.rowKeys.strip().split(",")
        reserved_column_name = options.reserved.strip().split(",")
        header = rowKey_name
        header.extend(reserved_column_name)
        of.write("\t".join(header) + "\n")
        result = key_content
        result.extend(list(reserved_content))
        of.write("\t".join(result) + "\n")
        value_and_count = []
        for name, value2count in name2value_and_count.iteritems():
            for value, count in value2count.iteritems():
                value_and_count.append(value)
                value_and_count.append(str(count))
            value_and_count.insert(0, name)
            of.write("\t".join(value_and_count) + "\n")
            value_and_count = []
    of.write("\n\ntotal line number : {} comments_empty_num : {}".format(line_num - 1, comments_empty_num))
    of.close()


# usage: python feature_distribution.py --rowKey "fnsku" --reserved "asin,product-name" --column "reason,customer-comments" --file "c-return.txt"
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-k", "--rowKeys", action="store", type="string", dest='rowKeys')
    parser.add_option("-c", "--column", action="store", type="string", dest='column')
    parser.add_option("-r", "--reserved", action="store", type="string", dest='reserved')
    parser.add_option("-f", "--file", action="store", type="string", dest='file')
    options, args = parser.parse_args()
    file = options.file
    handle_file(file, options);