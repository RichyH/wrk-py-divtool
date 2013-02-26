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
    regSearchV4DIR = re.compile(r'(^DIR).*\n(^\d\d[0-9 ]{3}).{48}([-=\w(,) ]*)[A-Z0-9:-=\s]*^[ ]{64}([-=\w(,) ]*)',re.I | re.M)
    regSearchV5DIR = re.compile(r'(^DIRECTORY NUMBER):.([0-9]{1,5}).*\n(^DIV STATE):.([A-Z, ]{1,}).*\n(^ADD INFO):.([-=\w(,) ]*)',re.I | re.M)
    items = []
    
#    print leseDatei("../../SUSIP_test.txt")
    datei = open("../../SUSIP_test.txt", "r")
    rawdata = datei.read()
    datei.close()
    del datei

    print 'V4:\n'
    result = regSearchV4DIR.finditer(rawdata)
    for dirs in result:
        print dirs.group(1) + ': [' + dirs.group(2) + '] [' + dirs.group(3) + '] [' + dirs.group(4) + ']'
    print '\nV5:\n'
    result = regSearchV5DIR.finditer(rawdata)
    for dirs in result:
        print dirs.group(1) + ': [' + dirs.group(2) + ']\t' + dirs.group(3) + ': [' + dirs.group(4) + ']\t' + dirs.group(5) + ': [' + dirs.group(6) + ']'
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