# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 14:48:15 2016

@author: hengyliu
"""

from lxml import html
import requests
import re
 
class ParseHtml:
    def __init__(self, url_file, outfile, url_unparse_file):
        self._urlSet = set()
        self.UrlInitial(url_file)
        self._head_p = '//span[@class="rendered_qtext"]'
        self._step_p = '//div[@class="pagedlist_item"]'
        self._subStep_p = './/div/span[@class="rendered_qtext"]/descendant::text()'
       
        self._sep = "*"
        self._outfile = outfile
        self._unparseUrl_file = url_unparse_file
    
    def UrlInitial(self, urlfile):
        with open(urlfile, 'r', encoding='utf-8') as fr:
            for line in fr:
                arr = line.split('\t')
                url = arr[0].strip()
                self._urlSet.add(url)
                
    def ParseHead(self):
        head = self._tree.xpath(self._head_p)
        head_res = head[0].text.strip('\n').strip()
        return head_res
      
    def ParseHead_2nd(self):
        _head_p = '//div[@class="category_title"]/h2[@class="header"]'
        head = self._tree.xpath(_head_p)
        head_res = head[0].text.strip('\n').strip()
        return head_res
      
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
        answer_res = ""
        StepCont = self._tree.xpath(self._step_p)
        for stepEle in StepCont:
            subStep = stepEle.xpath(self._subStep_p) 
            answer_res_ele = " ".join(subStep)
            answer_res_ele = answer_res_ele.replace('\n', ' ')
            answer_res_ele = re.sub(r'\s{2,}', ' ', answer_res_ele)
            answer_res_ele = answer_res_ele.strip('\n').strip()
            if(answer_res_ele != ""):
                answer_res += self._sep + answer_res_ele + '\n'        
        return answer_res
       # fw.write(self._sep + answer_res + '\n')
  
    def ParseStep_2nd(self, fw):
        StepCont = self._tree.xpath(self._step_p_2nd)
        answer_res = " ".join(StepCont)
        answer_res = answer_res.replace('\n', ' ')
        answer_res = re.sub(r'\s{2,}', ' ', answer_res)
        answer_res = answer_res.strip('\n').strip()
        return self._sep + answer_res + '\n'
        #fw.write(self._sep + answer_res + '\n')
  
    def Parse(self):
        fw = open(self._outfile, 'w', encoding='utf-8')
        fw_illegalUrl = open(self._unparseUrl_file, 'w', encoding='utf-8')
        
        for url in self._urlSet:
            
            try:
                result = self.ParseUrl(url, fw)
                fw.write(result)
            except:
                continue
                """                
                try:
                    result = self.ParseUrl_2nd(url, fw)
                    fw.write(result)
                except:    
                    continue
                """
        fw.close()
        fw_illegalUrl.close()
        
    def ParseUrl(self, url, fw):
        page = requests.get(url)
        self._tree = html.fromstring(page.content)      
        self._head = self.ParseHead()
        parseResult = url + '\n' + self._head + '\n'
        #fw.write(url + '\n')
        #fw.write(self._head + '\n')
        answer = self.ParseStep(fw)
        if answer.strip() == "":
            raise Exception("Empty")
        parseResult += answer
        return parseResult
       # fw.write(parseResult)
        
    def ParseUrl_2nd(self, url, fw):
        page = requests.get(url)
        self._tree = html.fromstring(page.content) 
        self._head = self.ParseHead()
        parseResult = url + '\n' + self._head + '\n'
        parseResult += self.ParseStep_2nd(fw)
        return parseResult
        
if __name__ == "__main__":
    ph = ParseHtml("C:/Code/data/Quora.Guide.cb64.txt", "C:/Code/data/QuoraParseResult.tsv", "C:/Code/data/QuoraUnableParseUrls.tsv")
    ph.Parse()
    
    
