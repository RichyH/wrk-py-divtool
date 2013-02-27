# coding=UTF-8
'''
Created on 21.02.2013

@author: Richy Hareter
No RegEx-Version
'''

def auswerten( element, position ):
                print str(position) + ':\t' + element


if __name__ == '__main__':
    datei = open("../../SUSIP_test.txt", "r")
    zeilen = datei.read().splitlines()
    datei.close()
    del datei

    elements = []
    i = 0
    
    for zeile in zeilen:
        elements += zeile.split()

    for e in elements:
        if (e != 'DIR' and e != 'DIRECTORY'):
            i += 1
            next
        else:
            auswerten(e,i)
            i += 1
        