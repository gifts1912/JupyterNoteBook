# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 14:15:06 2016

@author: hengyliu
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 11:17:59 2016

@author: hengyliu
"""

from lxml import html
import requests
import re
 
class ParseHtml:
    def __init__(self, url_file, outfile, url_unparse_file):
        self._urlSet = set()
        self.UrlInitial(url_file)
        self._head_p = '//h1[@class="content-title"]'
        self._description_p = '//div[@class="description"]'
        self._step_p = '//div[@id="ThreadAnswers"]//div[@class="msgBody wrapWord fullMessage"]/descendant::text()'
        self._step_p_2nd = '//div[@id="LastReply"]//div[@class="msgBody wrapWord fullMessage"]/descendant::text()'
       
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
        StepCont = self._tree.xpath(self._step_p)
        answer_res = " ".join(StepCont)
        answer_res = answer_res.replace('\n', ' ')
        answer_res = re.sub(r'\s{2,}', ' ', answer_res)
        answer_res = answer_res.strip('\n').strip()
        if(answer_res != ""):
            return self._sep + answer_res + '\n'
        else:
            return ""
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
                try:
                    result = self.ParseUrl_2nd(url, fw)
                    fw.write(result)
                except:    
                    continue
                """
                try:
                    result = self.ParseUrl_2nd(url, fw)
                    fw.write(result)
                except:
                    fw_illegalUrl.write(url + '\n')
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
    ph = ParseHtml("C:/Code/data/Support.microsoft.Guide.cb64_2.txt", "C:/Code/data/SupportMicrosoftParseResult_2.tsv", "C:/Code/data/SupportMicrosoftUnableParseUrls_2.tsv")
    ph.Parse()
    
    
