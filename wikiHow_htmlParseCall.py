# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 11:09:39 2016

@author: hengyliu
"""

from lxml import html
import requests
import re

class ParseHtml:
    def __init__(self, url_file, outfile, url_failParse_outfile):
        self._urlSet = set()
        self.UrlInitial(url_file)
        self._head_p = '//h1[@class="firstHeading"]/a'
        self._step_p = '//div[@class="section steps   sticky "]'
        self._sep = "*"
        self._outfile = outfile
        self._url_failParse_outfile = url_failParse_outfile
    
    def UrlInitial(self, urlfile):
        with open(urlfile, 'r', encoding='utf-8') as fr:
            for line in fr:
                arr = line.split('\t')
                url = arr[0].strip()
                self._urlSet.add(url)
                
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
        result = ""
        for ele in StepCont:#step1, step2
            #Title of Step1, Step2
            titles = ele.findall('.//*[@class="mw-headline"]')
            result += self._sep + titles[0].text + '\n'
            
            #Sub steps of Step1
            subPath = './/li/div[@class="step"]'   
            subSteps = ele.findall(subPath)
            for subEle in subSteps: #step1.1, step1.2
                #Title of step1.1
                subTitle = subEle.find('./b')
                sub_title = subTitle.text
                #fw.write(self._sep * 2 + sub_title + '\n')
                result += self._sep * 2 + sub_title + '\n'
                
                #Des of step1.1
                subEle_agin = subTitle.xpath('../text()')
                res = self.RemoveNullEle(subEle_agin)
                if res.strip():
                    #print (self._sep * 3 + self.RemoveNullEle(subEle_agin)) 
                    result += self._sep * 3 + self.RemoveNullEle(subEle_agin) + '\n'
                #sub step of step1.1
                sub_sub_txt = subTitle.xpath('../ul/li/text()')
                res = self.RemoveNullEle(sub_sub_txt)
                if res.strip():
                    #print (self._sep * 4 + self.RemoveNullEle(sub_sub_txt))
                    result += self._sep * 4 + self.RemoveNullEle(sub_sub_txt) + '\n'
        return result
        
    def ParseStep_2nd(self, fw):
        StepCont = self._tree.xpath(self._step_p)
        result = ""
        for ele in StepCont:#step1, step2
            #Title of Step1, Step2
            titles = ele.xpath('.//span[@class="mw-headline"]')
            result += self._sep + titles[0].text + '\n'
            #fw.write(self._sep + titles[0].text + '\n')
           
            #Sub steps of Step1
            sub_subStep_p = './/div/ol/li/div[@class="step"]'
            sub_subStep_nodes = ele.xpath(sub_subStep_p)
            for sub_subStep_node in sub_subStep_nodes:
                sub_infoes = sub_subStep_node.xpath('./descendant::text()')
                sub_info = " ".join(sub_infoes).replace('\n', ' ')
                sub_info = re.sub(r'\s{2,}', ' ', sub_info)
                sub_info = sub_info.strip('\n').strip()
                result += self._sep * 2 + sub_info + '\n'
                #fw.write(self._sep * 2 + sub_info + '\n')
        return result
                
    def Parse(self):
        fwUrl = open(self._url_failParse_outfile, 'w', encoding='utf-8')
        fw = open(self._outfile, 'w', encoding='utf-8')
        for url in self._urlSet:
            try:
                self.ParseUrl(url, fw)
            except:
                fwUrl.write(url + '\n')
        fw.close()
        fwUrl.close()
        
    def ParseUrl(self, url, fw):
        page = requests.get(url)
        self._tree = html.fromstring(page.content)      
        self._head = self.ParseHead() 
        result = url + '\n' + self._head + '\n'
        #fw.write(url + '\n')
        #fw.write(self._head + '\n')
        try:
            result += self.ParseStep(fw)
            fw.write(result)
        except:
            try:
                result += self.ParseStep_2nd(fw)
                fw.write(result)
            except:
                raise Exception("ParseFail")
       
        """
        try:
            result += self.ParseStep(fw)
            fw.write(result)
        except:
            try:
                result += self.ParseStep_2nd(fw)
                fw.write(result)
            except:
                raise Exception("ParseFailed")
        """
                
        
            
        
        
if __name__ == "__main__":
    ph = ParseHtml("C:/Code/data/wikihowcom.Guide.cb64_2.txt", "C:/Code/data/wikiHowParseResult_2.tsv", "C:/Code/data/wikiHowUnableParseUrls.txt")
    ph.Parse()
    
