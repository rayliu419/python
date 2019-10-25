# -*- coding: utf-8 -*-

# 用来学习cky算法的代码
# 实现了识别和parser功能，前者只判断是否句子能否被语法产生，后者还不仅判断，还要打印生成的语法树。
# 注意每个子串可能有多个归一的方式，在parser时，需要将不同的parser过程都要记下来。
# TODO：如果不是简单规则的CNF文法，怎么转化？ CNF文法仅仅包含A->BC, C->c的格式

cky_rules = [
    'S:NP VP',
    'PP:P NP',
    'VP:V NP',
    'VP:VP PP',
    'P:with',
    'V:saw',
    'NP:NP PP',
    'NP:astronomers',
    'NP:ears',
    'NP:saw',
    'NP:stars',
    'NP:telescopes'
]


def get_rule_left_right(rule):
    temp = rule.split(':')
    return temp[0], temp[1]


def get_symbol(item):
    rule = item[0]
    k, v = get_rule_left_right(rule)
    return k


def get_rule(item):
    return item[0]


def init_record_table(table, sentence):
    sentence_array = sentence.split(' ')
    sentence_length = len(sentence_array)
    for i in range(0, sentence_length):
        result_array = []
        for rule in cky_rules:
            k, v = get_rule_left_right(rule)
            if sentence_array[i] == v:
                result_array.append([rule, [i, i], [-1, -1]])
        table[i][i] = result_array


# 这里记录追溯结果的方式是使用index_i, index_j。注意对于某个字串，可能有多个符号生成，而上一层的字串在归一时，需要记住是从下层的哪个符号归一上去的。
# 如果不记录具体是哪个，回溯路径是会出错。
def record_rules(left, right, old_value, start, partition, end):
    result_array = []
    for index_i, i in enumerate(left):
        for index_j, j in enumerate(right):
            for rule in cky_rules:
                k, v = get_rule_left_right(rule)
                symobl_i = get_symbol(i)
                symobl_j = get_symbol(j)
                if (symobl_i + ' ' + symobl_j == v):
                    result_array.append([rule, [start, partition, index_i], [partition + 1, end, index_j]])
    if (len(old_value) != 0):
        result_array.extend(old_value)
    return result_array


def is_terminal(item):
    right = item[2]
    if (right[0]) == -1:
        return True
    return False


def is_start(item):
    return get_symbol(item) == 'S'


def parse(table, i, j, request_index):
    tree_index = 1
    for index, item in enumerate(table[i][j]):
        k, v = get_rule_left_right(get_rule(item))
        if (request_index != -1 and index != request_index):
            continue
        if (is_start(item)):
            print("\ntree {}".format(tree_index))
            tree_index += 1
            print(' S (', end='')
        elif(is_terminal(item)):
            print(' '+ v + ' ', end='')
            return
        symbols = v.split(' ')
        symbol1, symbol2 = symbols[0], symbols[1]
        print(' ' + symbol1 + ' ( ', end='')
        parse(table, item[1][0], item[1][1], item[1][2])
        print(' ) ', end='')
        print(' ' + symbol2 + ' ( ', end='')
        parse(table, item[2][0], item[2][1], item[2][2])
        print(' ) ', end='')


def parse_result(table, sentent_length):
    parse(table, 0, sentent_length - 1, -1)


def is_accept(table, sentence_length):
    for item in table[0][sentence_length - 1]:
        if (get_symbol(item) == 'S'):
            return True
    return False

# 不仅需要判断是否接受，还需要判断怎么parse出来的
def cky_parser(sentence):
    sentence_array = sentence.split(' ')
    sentence_length = len(sentence_array)
    table = [[[]] * sentence_length for row in range(0, sentence_length)]
    init_record_table(table, sentence)
    for length in range(2, sentence_length + 1):  # 自底向上计算可能的语法归一
        for start in range(0, sentence_length - length + 1):   # 计算文本串的起点
            for partition_offset in range(0, length - 1):      # 计算文本串分割的位置
                left = table[start][start + partition_offset]
                right = table[start + partition_offset + 1][start + length - 1]
                table[start][start + length - 1] = record_rules(left, right, table[start][start + length - 1], start, start + partition_offset, start + length - 1)
    if (is_accept(table, sentence_length)):
        print('\n=======================================================================================================')
        print('Accept - {}'.format(sentence))
        print('parse result')
        parse_result(table, sentence_length)
        print('\n=======================================================================================================')
    else:
        print('\n=======================================================================================================')
        print('Don\'t Accept - {}\n'.format(sentence))
        print('\n=======================================================================================================')


if __name__ == '__main__':
    sentence1 = "astronomers saw stars with ears"
    sentence2 = "saw stars"
    cky_parser(sentence1)
    cky_parser(sentence2)