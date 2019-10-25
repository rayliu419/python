# -*- coding: utf-8 -*-


# 数据使用https://courses.cs.washington.edu/courses/cse590a/09wi/pcfg.pdf
# 可以利用画出来的树来看答案是不是对了
# PCKY的实践,不仅会parse多个结果，需要考虑每棵树产生的可能性

cky_rules = [
    'S:NP VP:1.0',
    'PP:P NP:1.0',
    'VP:V NP:0.7',
    'VP:VP PP:0.3',
    'P:with:1.0',
    'V:saw:1.0',
    'NP:NP PP:0.4',
    'NP:astronomers:0.1',
    'NP:ears:0.18',
    'NP:saw:0.04',
    'NP:stars:0.18',
    'NP:telescopes:0.1'
]


def get_rule_part(rule):
    temp = rule.split(':')
    return temp[0], temp[1], float(temp[2])


def get_symbol(item):
    rule = item[0]
    left, right, probability = get_rule_part(rule)
    return left


def get_symbol_and_probability(item):
    rule = item[0]
    left, right, _ = get_rule_part(rule)
    probability = item[3]
    return left, float(probability)


def get_rule(item):
    return item[0]


def is_terminal(item):
    right = item[2]
    if (right[0]) == -1:
        return True
    return False


def is_start(item):
    return get_symbol(item) == 'S'


def init_record_table(table, sentence):
    sentence_array = sentence.split(' ')
    sentence_length = len(sentence_array)
    for i in range(0, sentence_length):
        result_array = []
        for rule in cky_rules:
            k, v, probability = get_rule_part(rule)
            if sentence_array[i] == v:
                result_array.append([rule, [i, i], [-1, -1], probability])
        table[i][i] = result_array


# 这里记录追溯结果的方式是使用index_i, index_j。注意对于某个字串，可能有多个符号生成，而上一层的字串在归一时，需要记住是从下层的哪个符号归一上去的。
# 如果不记录具体是哪个，回溯路径是会出错。
def record_rules(left, right, old_value, start, partition, end):
    result_array = []
    for index_i, i in enumerate(left):
        for index_j, j in enumerate(right):
            for rule in cky_rules:
                k, v, probability = get_rule_part(rule)
                symobl_i, probability1 = get_symbol_and_probability(i)
                symobl_j, probability2 = get_symbol_and_probability(j)
                if (symobl_i + ' ' + symobl_j == v):
                    # 注意item中的第四项的概率是规则本身的概率 * 左边子树根据所有规则生成的概率 * 右边子树根据所有规则生成的概率
                    result_array.append([rule, [start, partition, index_i], [partition + 1, end, index_j], probability * probability1 * probability2])
    if (len(old_value) != 0):
        result_array.extend(old_value)
    return result_array


def parse(table, i, j, request_index):
    tree_index = 1
    for index, item in enumerate(table[i][j]):
        k, v, _ = get_rule_part(get_rule(item))
        if (request_index != -1 and index != request_index):
            continue
        if (is_start(item)):
            _, probability = get_symbol_and_probability(item)
            print('\ntree {} probability : {}'.format(tree_index, probability))
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
def pcky_parser(sentence):
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
    pcky_parser(sentence1)