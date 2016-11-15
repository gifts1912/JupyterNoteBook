# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 21:40:20 2016

@author: hengyliu
"""

import numpy as np
import math

def loadDataSet(fileName):
    fr = open(fileName, 'r', encoding='utf-8')
    dataMat = []; labelMat = []
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        dataMat.append([float(lineArr[0]), float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    fr.close()
    return dataMat, labelMat
    

def selectJrand(i, m):
    j = i
    while j == i:
        j = int(np.random.uniform(0, m))
    return j
    
def clipAlpha(aj, H, L):
    if aj > H:
        aj = H
    if L > aj:
        aj = L
    return aj
    
    
def smoSimple(dataMatIn, classLabels, C, toler, maxIter):
    dataMatrix = np.mat(dataMatIn); labelMat = np.mat(classLabels).transpose()
    b = 0.1; m, n = np.shape(dataMatrix)
    alphas = np.mat(np.zeros((m, 1)) + 0.1)
    ite = 0
    while(ite < maxIter):
        alphaPairsChanged = 0
        for i in range(m):
            fXi = float(np.multiply(labelMat, alphas).T * (dataMatrix * dataMatrix[i,:].T)) + b
            Ei = fXi - float(labelMat[i])
            if ((labelMat[i]*Ei < -toler) and (alphas[i] <C)) or ((labelMat[i] * Ei > toler) and (alphas[i] > 0)):         
                j = selectJrand(i, m)
                fXj = float(np.multiply(labelMat, alphas).T * (dataMatrix * dataMatrix[j,:].T)) + b
                Ej = fXj - float(labelMat[i])
                alphaIOld = float(alphas[i])
                alphaJOld = float(alphas[j])
                if float(labelMat[i]) != float(labelMat[j]):
                    L = max(0, alphas[j] - alphas[i])
                    H = min(C, C + alphas[j] - alphas[i])
                else:
                    L = max(0, alphas[j] + alphas[i] - C)
                    H = min(C, alphas[j] + alphas[i])
                if L == H:
                    print ("L == H")
                    continue
                eta = 2.0 * dataMatrix[i,:] * dataMatrix[j,:].T - dataMatrix[i,:] * dataMatrix[i,:].T - dataMatrix[j,:] * dataMatrix[j,:].T
                if eta >= 0:
                    print("eta == 0")
                    continue
                alphas[j] -= labelMat[j] * (Ei - Ej) / eta
                alphas[j] = clipAlpha(alphas[j], H, L)
                if(abs(alphas[j] - alphaJOld < 0.00001)):
                    print("j not moving enough")
                    continue
                alphas[i] += labelMat[i] * labelMat[j] * (alphaJOld - alphas[j])
                
                b1 = b - Ei - labelMat[i] * (alphas[i] - alphaIOld)*dataMatrix[i,:]*dataMatrix[i,:].T - labelMat[j]*(alphas[j] - alphaJOld)* dataMatrix[i,:] \
* dataMatrix[j,:].T
                b2 = b - Ej - labelMat[i] * (alphas[i] - alphaIOld)*dataMatrix[i,:]*dataMatrix[j,:].T - labelMat[j]*(alphas[j] - alphaJOld)*dataMatrix[j,:] \
*dataMatrix[j,:].T
                if alphas[i] > 0 and alphas[i] < C:
                    b = b1
                elif alphas[j] > 0 and alphas[j] < C:
                    b = b2
                else:
                    b = (b1 + b2)/2.0
                alphaPairsChanged += 1
                
                print("iter:%d i:%d, pair changed %d"%(ite, i, alphaPairsChanged))
        if alphaPairsChanged == 0:
            ite += 1
        else:
            ite = 0
        print("iteration number:{0}".format(ite))
    return b, alphas