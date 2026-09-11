# -*- coding: UTF-8 -*-
import numpy as np
from functools import reduce

"""
函数说明:创建实验样本。词表到向量的转换函数

Parameters:
	无
Returns:
	postingList - 实验样本切分的词条
	classVec - 类别标记向量

"""
def loadDataSet():
	postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],				#切分的词条
				['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
				['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
				['stop', 'posting', 'stupid', 'worthless', 'garbage'],
				['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
				['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
	classVec = [0,1,0,1,0,1]   																#类别标记向量，1代表侮辱性词汇，0代表不是
	return postingList,classVec																#返回实验样本切分的词条和类别标记向量

"""
函数说明:创建词汇列表。将切分的实验样本词条整理成不重复的词条列表，也就是创建词汇列表

Parameters:
	dataSet - 整理的样本数据集
Returns:
	vocabSet - 返回不重复的词条列表，也就是词汇表

"""
#创建词汇表，文档向量化的第一步
def createVocabList(dataSet):
	vocabSet = set([])  					#创建一个空的不重复列表
	for document in dataSet:				
		vocabSet = vocabSet | set(document) #取并集
	return list(vocabSet)

"""
函数说明:文档集合向量化。根据词汇列表，将inputSet文档集合向量化，向量的每个元素为1或0

Parameters:
	vocabList - createVocabList返回的列表，词汇表
	inputSet - 切分的词条列表，输入集
Returns:
	returnVec - 文档向量,词集模型

"""
#词汇法，文档向量化第二步
def setOfWords2Vec(vocabList, inputSet):
	returnVec = [0] * len(vocabList)									#创建一个其中所含元素都为0的向量
	for word in inputSet:												#遍历每个词条
		if word in vocabList:											#如果词条存在于词汇表中，则置1
			returnVec[vocabList.index(word)] = 1
		else:
			print("the word: %s is not in my Vocabulary!" % word)       #一般不可能出现，词汇列表里肯定有
	return returnVec													#返回文档向量


"""
函数说明:计算条件概率。朴素贝叶斯分类器训练函数，计算条件概率

拉普拉斯平滑：防止由于某一个条件概率为0，导致分类概率为0的不合理情形
条件概率对数化：防止小数相乘出现的下溢出问题

Parameters:
    trainMatrix - 训练文档矩阵，即setOfWords2Vec文档向量返回的returnVec构成的矩阵
    trainCategory - 训练类别标记向量，即loadDataSet词表到向量的转换函数返回的classVec标记
Returns:
    p0Vect - 侮辱类的条件概率数组
    p1Vect - 非侮辱类的条件概率数组
    pAbusive - 文档属于侮辱类的概率

"""
def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)                            #计算训练的文档数目6
    numWords = len(trainMatrix[0])                            #计算文档的词条数32
    pAbusive = sum(trainCategory)/float(numTrainDocs)        #文档属于侮辱类的概率
    p0Num = np.ones(numWords); p1Num = np.ones(numWords)    #创建numpy.ones数组,词条出现数初始化为1，拉普拉斯平滑
    p0Denom = 2.0; p1Denom = 2.0                            #分母初始化为2,拉普拉斯平滑
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:                            #统计属于侮辱类的条件概率所需的数据，即P(w0|1),P(w1|1),P(w2|1)···
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:                                                #统计属于非侮辱类的条件概率所需的数据，即P(w0|0),P(w1|0),P(w2|0)···
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = np.log(p1Num/p1Denom)                            #取对数，防止下溢出
    p0Vect = np.log(p0Num/p0Denom)
    return p0Vect,p1Vect,pAbusive                            #返回属于侮辱类的条件概率数组，属于非侮辱类的条件概率数组，文档属于侮辱类的概率

"""
函数说明:朴素贝叶斯分类器分类函数

Parameters:
    vec2Classify - 待分类的词条数组
    p0Vec - 侮辱类的条件概率数组
    p1Vec -非侮辱类的条件概率数组
    pClass1 - 文档属于侮辱类的概率
Returns:
    0 - 属于非侮辱类
    1 - 属于侮辱类

"""
def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + np.log(pClass1)        #对应元素相乘。logA * B = logA + logB，所以这里加上log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + np.log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0

"""
函数说明:测试函数。测试朴素贝叶斯分类器

P(侮辱类|stupid,garbage)=P(stupid|侮辱类)xP(garbage|侮辱类)xP(侮辱类)
P(非侮辱类|stupid,garbage)=P(stupid|非侮辱类)xP(garbage|非侮辱类)xP(非侮辱类)
比较上述两个值得大小，确定是哪一类。

Parameters:
	无
Returns:
	无

"""
def testingNB():
	listOPosts,listClasses = loadDataSet()									#创建实验样本
	myVocabList = createVocabList(listOPosts)								#创建词汇表，set为无序集，每次运行结果不同
	trainMat=[]
	for postinDoc in listOPosts:
		trainMat.append(setOfWords2Vec(myVocabList, postinDoc))				#将实验样本向量化
	p0V,p1V,pAb = trainNB0(np.array(trainMat),np.array(listClasses))		#训练朴素贝叶斯分类器

	testEntry = ['love', 'my', 'dalmation']									#测试样本1
	thisDoc = np.array(setOfWords2Vec(myVocabList, testEntry))				#测试样本向量化
	if classifyNB(thisDoc,p0V,p1V,pAb):
		print(testEntry,'属于侮辱类')										#执行分类并打印分类结果
	else:
		print(testEntry,'属于非侮辱类')										#执行分类并打印分类结果

	testEntry = ['stupid', 'garbage']										#测试样本2
	thisDoc = np.array(setOfWords2Vec(myVocabList, testEntry))				#测试样本向量化
	if classifyNB(thisDoc,p0V,p1V,pAb):
		print(testEntry,'属于侮辱类')										#执行分类并打印分类结果
	else:
		print(testEntry,'属于非侮辱类')										#执行分类并打印分类结果

if __name__ == '__main__':
	postingList, classVec = loadDataSet()
	myVocabList = createVocabList(postingList)
	print('myVocabList:\n', myVocabList)
	trainMat = []
	for postinDoc in postingList:
		trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
	p0V, p1V, pAb = trainNB0(trainMat, classVec)
	print('p0V:\n', p0V)
	print('p1V:\n', p1V)
	#print('classVec:\n', classVec)
	#print('pAb:\n', pAb)
	testingNB()