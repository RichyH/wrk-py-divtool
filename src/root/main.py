# coding=UTF-8
'''
Created on 21.02.2013

@author: Richy Hareter
'''
import re

def leseDatei(datei): 
    d = {} 
    f = open(datei,"r") 
    for zeile in f: 
        if ":" in zeile: 
            key, d[key] = (s.strip() for s in zeile.split(r':')) 
        elif "key" in locals(): 
            d[key] += "\n%s" % zeile.strip() 
    f.close()
    return d

if __name__ == '__main__':
    regSplit = re.compile(r'\t|\n')
    regSearch = re.compile(r'\A.*',re.I | re.M)
    items = []
    
#    print leseDatei("../../SUSIP_test.txt")
    datei = open("../../SUSIP_test.txt", "r")
        
#    for zeile in datei:
#        items.append(re.split(regSplit,zeile))
#    for item in items:
#        print item
    rawdata = datei.read()
    datei.close()

    m = regSearch.search(rawdata)
    print m.expand()
    print 'Ende'
#    del datei, zeile







'''
#   Spaß mit Rekursion
    def druck(l,s):
        if l > 0:
            print l,'x',s
            return druck(l-1,s*l)
        else:
            return 0,'x',s
    
    rest = druck(4,"Mauzi")
    for i, string in enumerate(rest):
        print string,
    print ''
'''