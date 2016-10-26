# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 11:58:22 2016

@author: hengyliu
"""
from lxml import html
import requests
import re
 
class ParseHtml:
    def __init__(self, url_file, outfile, url_unparse_file):
        self._urlSet = set()
        self.UrlInitial(url_file)
        self._head_p = '//div[@class="codeIdentifier"]/descendant::text()'
        self._description_p = '//div[@class="description"]'
        self._step_p = '//ul[@class="contentBlurb definitionList"]/li'
        self._sep = "*"
        self._outfile = outfile
        self._unparseUrl_file = url_unparse_file
    
    def UrlInitial(self, urlfile):
        with open(urlfile, 'r', encoding='utf-8') as fr:
            for line in fr:
                arr = line.split('\t')
                url = arr[0].strip()
                self._urlSet.add(url + '?ALLSTEPS')
                
    def ParseHead(self):
        head = self._tree.xpath(self._head_p)
        return head[0]
      
    def ParseDescription(self):
        des = self._tree.xpath(self._description_p)
       # print (des[0].atrrib)
        return des[0].text
    
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
            subStepMerge = ele.xpath('./descendant::text()')
            subStepMerge = ' '.join(subStepMerge).replace('\n', ' ')
            subStepMerge = re.sub(r'\s{2,}', ' ', subStepMerge)
            fw.write(self._sep + subStepMerge + '\n')
            '''
            for subStep_ele in subSteps:
                subStep_ele = subStep_ele.strip('\n').strip()
                fw.write(self._sep * 2 + subStep_ele + '\n')
            '''
            """for subEle in subSteps: #step1.1, step1.2
                #Title of step1.1
                step_body = subEle[0].text
                fw.write(self._sep * 2 + step_body + '\n')
            """
    def Parse(self):
        fw = open(self._outfile, 'w', encoding='utf-8')
        fw_illegalUrl = open(self._unparseUrl_file, 'w', encoding='utf-8')
        
        for url in self._urlSet:
            try:
                self.ParseUrl(url, fw)
            except:
                fw_illegalUrl.write(url + '\n')
        fw.close()
        fw_illegalUrl.close()
        
    def ParseUrl(self, url, fw):
        page = requests.get(url)
        self._tree = html.fromstring(page.content)      
        self._head = self.ParseHead()      
        fw.write(url + '\n')
        des = self.ParseDescription()
        fw.write(self._head + '\n' + des + '\n')   
        self.ParseStep(fw)
        
if __name__ == "__main__":
    ph = ParseHtml("C:/Code/data/icd9data.Guide.cb64.txt", "C:/Code/data/icd9dataParseResult.tsv", "C:/Code/data/icd9dataUnableParseUrls.tsv")
    ph.Parse()
    
