# coding=UTF-8
'''
Created on 21.02.2013

@author: Richy Hareter
'''

if __name__ == '__main__':
    datei = open("../../SUSIP_test.txt", "r")
    for zeile in datei:
            print zeile
            if raw_input("") == "q":
                break
# Und jetzt kommt der Spass mit der RegEx ;)            
    datei.close()
    del datei, zeile







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