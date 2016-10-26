# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 18:44:30 2016

@author: hengyliu
"""
from lxml import html
import requests
 
class ParseHtml:
    def __init__(self, url, outfile):
        self._url = url
        self._head_p = '//h1[@class="firstHeading"]/a'
        self._step_p = '//*[@class="section steps   sticky "]'
        self._sep = "*"
        self._outfile = outfile
 
    def ParseHead(self):
        head = self._tree.xpath(self._head_p)
        return head[0].text
        
    def RemoveNullEle(self, des_list):
        res = []
        for ele in des_list:
            if ele.strip(' ').strip('\n'):
                res.append(ele)
        return ''.join(res)

    def ParseStep(self, fw):
        StepCont = self._tree.xpath(self._step_p)
        for ele in StepCont:#step1, step2
            #Title of Step1, Step2
            titles = ele.findall('.//*[@class="mw-headline"]')
            fw.write(self._sep + titles[0].text + '\n')
            
            #Sub steps of Step1
            subPath = './/li/div[@class="step"]'   
            subSteps = ele.findall(subPath)
            for subEle in subSteps: #step1.1, step1.2
                #Title of step1.1
                subTitle = subEle.find('./b')
                sub_title = subTitle.text
                #print(self._sep * 2 + sub_title)
                fw.write(self._sep * 2 + sub_title + '\n')
                
                #Des of step1.1
                subEle_agin = subTitle.xpath('../text()')
                res = self.RemoveNullEle(subEle_agin)
                if res.strip():
                    #print (self._sep * 3 + self.RemoveNullEle(subEle_agin)) 
                    fw.write(self._sep * 3 + self.RemoveNullEle(subEle_agin) + '\n')
                #sub step of step1.1
                sub_sub_txt = subTitle.xpath('../ul/li/text()')
                res = self.RemoveNullEle(sub_sub_txt)
                if res.strip():
                    #print (self._sep * 4 + self.RemoveNullEle(sub_sub_txt))
                    fw.write(self._sep * 4 + self.RemoveNullEle(sub_sub_txt) + '\n')
        
    def Parse(self):
        page = requests.get(self._url)
        self._tree = html.fromstring(page.content)
        
        fw = open(self._outfile, 'w', encoding='utf-8')
        self._head = self.ParseHead()      
        fw.write(self._url + '\n')
        fw.write(self._head + '\n')
        self.ParseStep(fw)
        fw.close()
        
if __name__ == "__main__":
    ph = ParseHtml("http://www.wikihow.com/Treat-Carpet-Burns", "C:/Code/data/wikiHowParseResult.tsv")
    ph.Parse()
    