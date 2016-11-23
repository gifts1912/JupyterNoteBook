# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 10:35:55 2016

@author: hengyliu
"""

import numpy as np

def loadData():
    datMat = np.mat([[1, 2.1], [2.0, 1.1], [1.3, 1.0], [1, 1.0], [2.0, 1.0]])
    classLabels = [1.0, 1.0, -1.0, -1.0, 1.0]
    return datMat, classLabels
    
def stumpClassify(dataMatrix, dimen, threshVal, threshIneq):
    m = dataMatrix.shape[0]
    labelsVec = np.ones((m, 1))
    if threshIneq == "lt":
        labelsVec[dataMatrix[:,dimen] <= threshVal] = -1
    elif threshIneq == "gt":
        labelsVec[dataMatrix[:,dimen] > threshVal] = -1
    else:
        print("not correct of threshIneq: {0}".format(threshIneq))
        return
    return labelsVec
    
def buildStump(datArr, classLabels, D):
    datMat = np.mat(datArr); classLabels = np.mat(classLabels).T
    stepNum = 10.0
    m, n = datMat.shape()
    bestClassEst = np.mat(np.zeros((m, 1))); bestStump = {}; minErr = np.inf 
    for j in range(len(n)):
        rangeMin = datMat[:, j].min(); rangeMax = datMat[:,j].max()
        stepSize = (rangeMax - rangeMin)/stepNum
        for s in range(-1, int(stepNum) + 1):
            for inequle in ['lt', 'gt']:
                thresh = rangeMin + float(s) * stepSize
                predictedVec = stumpClassify(datMat, j, thresh, inequle)
                errArr = np.mat(np.zeros((m, 1)))
                errArr[classLabels != predictedVec] = 1
                errWei = errArr * D.T
                if errWei < minErr:
                    minErr = errWei
                    bestClassEst = predictedVec.copy()
                    bestStump['dim'] = j
                    bestStump['ineq'] = inequle

    return bestStump, minErr, bestClassEst
            
        