# coding=UTF-8
'''
Created on 21.02.2013

@author: Richy Hareter
'''
import re

if __name__ == '__main__':
    regSplit = re.compile(r'\t|\n')
    regSearchV4DIRs = re.compile(r'(^DIR).*\n(^\d\d[0-9 ]{3}).{48}([-=\w(,) ]*)[A-Z0-9:-=\s]*',re.I | re.M)
    regSearchV4DIRl = re.compile(r'(^DIR).*\n(^\d\d[0-9 ]{3}).{48}([-=\w(,) ]*)[A-Z0-9:-=\s]*^[ ]{64}([-=\w(,) ]*)',re.I | re.M)
    regSearchV5DIR = re.compile(r'(^DIRECTORY NUMBER):.([0-9]{1,5}).*\n(^DIV STATE):.([A-Z, ]{1,}).*\n(^ADD INFO):.([-=\w(,) ]*)',re.I | re.M)
    items = []
    
    datei = open("../../SUSIP_test.txt", "r")
    rawdata = datei.read()
    datei.close()
    del datei

    print 'V4:\n'
    result = regSearchV4DIRs.finditer(rawdata)
    for dirs in result:
        print dirs.group(1) + ': [' + dirs.group(2) + '] [' + dirs.group(3) + ']'
    print '\n'
    result = regSearchV4DIRl.finditer(rawdata)
    for dirs in result:
        print dirs.group(1) + ': [' + dirs.group(2) + '] [' + dirs.group(3) + '] [' + dirs.group(4) + ']'
    print '\nV5:\n'
    result = regSearchV5DIR.finditer(rawdata)
    for dirs in result:
        print dirs.group(1) + ': [' + dirs.group(2) + ']\t' + dirs.group(3) + ': [' + dirs.group(4) + ']\t' + dirs.group(5) + ': [' + dirs.group(6) + ']'
    print 'Ende'

