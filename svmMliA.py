# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 21:40:20 2016

@author: hengyliu
"""

from numpy import *
import math
import numpy as np

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
    dataMatrix = mat(dataMatIn); labelMat = mat(classLabels).transpose()
    b = 0; m,n = shape(dataMatrix)
    alphas = mat(zeros((m,1)))
    iter = 0
    while (iter < maxIter):
        alphaPairsChanged = 0
        for i in range(m):
            fXi = float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[i,:].T)) + b
            Ei = fXi - float(labelMat[i])#if checks if an example violates KKT conditions
            if ((labelMat[i]*Ei < -toler) and (alphas[i] < C)) or ((labelMat[i]*Ei > toler) and (alphas[i] > 0)):
                j = selectJrand(i,m)
                fXj = float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[j,:].T)) + b
                Ej = fXj - float(labelMat[j])
                alphaIold = alphas[i].copy(); alphaJold = alphas[j].copy();
                if (labelMat[i] != labelMat[j]):
                    L = max(0, alphas[j] - alphas[i])
                    H = min(C, C + alphas[j] - alphas[i])
                else:
                    L = max(0, alphas[j] + alphas[i] - C)
                    H = min(C, alphas[j] + alphas[i])
                if L==H:
                    print ("L==H")
                    continue
                eta = 2.0 * dataMatrix[i,:]*dataMatrix[j,:].T - dataMatrix[i,:]*dataMatrix[i,:].T - dataMatrix[j,:]*dataMatrix[j,:].T
                if eta >= 0: print ("eta>=0"); continue
                alphas[j] -= labelMat[j]*(Ei - Ej)/eta
                alphas[j] = clipAlpha(alphas[j],H,L)
                if (abs(alphas[j] - alphaJold) < 0.00001): print ("j not moving enough"); continue
                alphas[i] += labelMat[j]*labelMat[i]*(alphaJold - alphas[j])#update i by the same amount as j
                                                                        #the update is in the oppostie direction
                b1 = b - Ei- labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[i,:].T - labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[i,:]*dataMatrix[j,:].T
                b2 = b - Ej- labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[j,:].T - labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[j,:]*dataMatrix[j,:].T
                if (0 < alphas[i]) and (C > alphas[i]): b = b1
                elif (0 < alphas[j]) and (C > alphas[j]): b = b2
                else: b = (b1 + b2)/2.0
                alphaPairsChanged += 1
                print ("iter: %d i:%d, pairs changed %d" % (iter,i,alphaPairsChanged))
        if (alphaPairsChanged == 0): iter += 1
        else: iter = 0
        print ("iteration number: %d" % iter)
    return b,alphas
    
    
class optStruct:
    def __init__(self, dataMatIn, labelMatIn, C, toler):
        self.X = np.mat(dataMatIn)
        self.labels = np.mat(labelMatIn).transpose()
        self.m = np.shape(dataMatIn)[0]
        self.alphas = np.mat(np.zeros(self.m, 1))
        self.eCache = np.mat(np.zeros(self.m, 2))
        self.b = 0
        self.C = C
        self.tol = toler
        
        
    def calcEk(self, k):
        fxk = float(np.multiply(self.labels, self.alphas).T * (self.X * self.X[k,:].T)) + self.b
        Ek = fxk - float(self.labels[k])
        return Ek
        
    def selectJ(self, i, Ei):
        self.eCache[i] = [1, Ei]
        validList = np.nonzero((self.eCache[:, 0].A))[0]
        maxDeltaE = 0; maxK = -1; Ej = 0
        if len(validList) > 1:
            for k in validList:
                if k == i:
                    continue
                Ek = self.calcEk(k)
                deltaE = abs(Ek - Ei)
                if maxDeltaE < deltaE:
                    maxDeltaE = deltaE; maxK = k; Ej = Ek
            return maxK, Ej
        else:
            j = selectJrand(i, self.m)
            Ej = self.calcEk(j)
        return j, Ej
        
    def updateEk(self, k):
        Ek = self.calcEk(k)
        self.eCache[k] = [1, Ek]


    def innerL(self, i):
        Ei = self.calcEk(i)
        if ((self.labels[i] * Ei < -1.0 * self.tol) and (self.alphas[i] < self.C)) or ((self.labels[i] * Ei > self.tol) and (self.alphas[i] > 0)):
            j, Ej = self.selectJ(i, Ei)
            alphaIold = self.alphas[i].copy(); alphaJold = self.alphas[j].copy()
            if (self.labels[i] != self.labels[j]):
                L = max(0, self.alphas[j] - self.alphas[i])
                H = min(self.C, self.C + self.alphas[j] - self.alphas[i])
            else:
                L = max(0, self.alphas[i] + self.alphas[j] - self.C)
                H = min(C, self.alphas[i] + self.alphas[j])
            if (L == H): print("L == H"); return 0
            eta = 2 * (self.X[j,:] * self.X[:,i].T) - self.X[i,:] * self.X[i,:].T - self.X[j,:] * self.X[j,:].T
            if eta >= 0: print("eta >= 0"); return 0
            self.alphas[j] -= self.labels[j] * (Ei - Ej)/eta
            self.alphas[j] = clipAlpha(self.alphas[j], H, L)
            if abs(self.alphas[j] - alphaJold) < 0.00001:
                print ("j not moving"); return 0
            self.alphas[i] += (self.labels[i] *self.labels[j]) * (alphaJold - self.alphas[j])
            self.updateEk(i)
            
            b1 = self.b - Ei - self.labels[i]*(self.alphas[i] - alphaIold)*(self.X[i,:] * self.X[i,:].T) - self.labels[j]*(self.alphas[j] - alphaJold)*self.X[i,:] * self.X[j,:].T
            b2 = self.b - Ej - self.labels[i]*(self.alphas[i] - alphaIold) * (self.X[i,:] * self.X[j,:].T) - self.labels[j] * (self.alphas[j] - alphaJold)*self.X[j,:] * self.X[j,:].T
            
            if (0 < self.alphas[i]) and (self.alphas[i] < self.C):
                b = b1
            elif (0 < self.alphas[j]) and (self.alphas[j] < self.C):
                b = b2
            else:
                b = (b1 + b2)/2.0
            return 1
        else:
            return 0
    
                    
        