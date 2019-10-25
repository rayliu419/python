#coding=utf-8

import sys
import math
import copy
'''
    类似于kd-tree.
'''

class KdNode():
    def __init__(self, nodeDataList, kdRange, split, splitValue, left, right):
        self.nodeDataList = nodeDataList
        self.kdRange = kdRange
        self.split = split
        self.splitValue = splitValue
        self.left = left
        self.right = right
        self.parent = None
class KdTree():
    def __init__(self):
        self.root = None

    '''
        获取dataList的取值范围.
    '''
    def getRange(self,dataList):
        minVector = copy.deepcopy(dataList[0])
        maxVector = copy.deepcopy(dataList[0])

        for data in dataList:
            for i in range(0, len(data)):
                if minVector[i] > data[i]:
                    minVector[i] = data[i]
                if maxVector[i] < data[i]:
                    maxVector[i] = data[i]
        return [minVector, maxVector]


    '''
        获取最佳的分割点.
    '''
    def getBestSplit(self, dataList):
        avgList = [0] * len(dataList[0])
        dataLen = len(dataList)

        varList = [0] * len(dataList[0])


        for data in dataList:
            for i in range(0, len(data)):
                avgList[i] += data[i]
        for i in range(0, len(avgList)):
            avgList[i] = (avgList[i] + 0.0) / dataLen

        for data in dataList:
            for i in range(0, len(data)):
                varList[i] += (data[i] - avgList[i]) * (data[i] - avgList[i])
        for i in range(0, len(varList)):
            varList[i] = (varList[i] + 0.0 ) / dataLen

        splitIndex = 0
        splitValue = varList[0]

        for i in range(0, len(varList)):
            if splitValue <= varList[i]:
                splitIndex = i
                splitValue = varList[i]
        return splitIndex


    def getDistance(self,data1, data2):
        distance = 0.0
        for i in range(0, len(data1)):
            distance += (data1[i] - data2[i]) * (data1[i] - data2[i])
        return math.sqrt(distance)


    '''
        选出距离一点距离最近的点.
    '''
    def getNearestPoint(self, dataList, dataNode):
        minDist = self.getDistance(dataList[0], dataNode)
        minData = dataList[0]

        for data in dataList:
            dist = self.getDistance(data, dataNode)
            if minDist >= dist:
                minDist = dist
                minData = data
        return minData, minDist


    def splitData(self, splitValue, splitIndex, dataList):
        leftDataList = []
        rightDataList = []

        for data in dataList:
            if data[splitIndex] > splitValue:
                rightDataList.append(data)
            else:
                leftDataList.append(data)
        return leftDataList, rightDataList


    def buildKDTree(self, dataList):
        self.root =  self.createKDTree(dataList)


    def createKDTree(self, dataList):

        kdRange = self.getRange(dataList)

        if len(dataList) <= 10:
            return KdNode(dataList, kdRange, None,None, None, None)


        # 获取分割的维度.
        splitIndex = self.getBestSplit(dataList)

        # 获取分割的维度上的分割值.
        splitValue = (kdRange[0][splitIndex] + kdRange[1][splitIndex] + 0.0) / 2

        # 对当前数据进行切分.
        leftDataList, rightDataList = self.splitData(splitValue, splitIndex, dataList)


        node = KdNode([], kdRange, splitIndex, splitValue, leftDataList, rightDataList)

        # 创建子节点.
        node.left = self.createKDTree(leftDataList)
        node.right = self.createKDTree(rightDataList)

        # 填充父亲节点.
        node.left.parent = node
        node.right.parent = node

        return node


    '''
        正确答案来自于知乎,  有正确的逻辑推理: https://www.zhihu.com/question/49064063
    '''
    def checkIsIn(self, point, round, kdRange):
        nearPoint = [0] * len(point)

        pointSize = len(point)
        for i in range(0, pointSize):
            minValue = kdRange[0][i]
            maxValue = kdRange[1][i]

            if point[i] < minValue:
                nearPoint[i] = minValue
            elif point[i] > maxValue:
                nearPoint[i] = maxValue
            else:
                nearPoint[i] = point[i]

        dist = self.getDistance(nearPoint, point)
        if dist <= round:
            return True
        return False

    '''
        寻找距离最近的点.
    '''
    def searchNearestNode(self, key, node):
        if len(node.nodeDataList) != 0:
            return self.getNearestPoint(node.nodeDataList, key)
        # 首先获取底部的数据最近的点.
        isRight = False
        if key[node.split] > node.splitValue:
            childData, childDist = self.searchNearestNode(key, node.right)
            isRight = True
        else:
            childData, childDist = self.searchNearestNode(key, node.left)

        # 查看当前的右边是否有相交.
        if not isRight:
            isCross = self.checkIsIn(childData, childDist, node.right.kdRange)
            if isCross:
                newChildData, newChildDist = self.searchNearestNode(key, node.right)
                if childDist > newChildDist:
                    childDist = newChildDist
                    childData = newChildData
        # 查看当前的左边是否有相交.
        if isRight:
            isCross = self.checkIsIn(childData, childDist, node.left.kdRange)
            if isCross:
                newChildData, newChildDist = self.searchNearestNode(key, node.left)
                if childDist > newChildDist:
                    childDist = newChildDist
                    childData = newChildData

        return childData, childDist



if __name__ == "__main__":
    # 测试.
    tree = KdTree()
    dataList = []

    dataList.append([1,4,1])
    dataList.append([4,2,2])
    dataList.append([5,8,1])
    dataList.append([7,9,2])
    dataList.append([10,11,1])

    dataList.append([1,5,2])
    dataList.append([1,9,1])
    dataList.append([12,11,2])
    dataList.append([18,12,1])
    dataList.append([12,3,2])
    dataList.append([28,9,1])
    dataList.append([10,10,2])
    dataList.append([8,8,1])

    tree.buildKDTree(dataList)

    nearest, nearestDist = tree.searchNearestNode([3,9,3], tree.root)

    print(nearest, nearestDist)
