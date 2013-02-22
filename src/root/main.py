'''
Created on 21.02.2013

@author: Richy Hareter
'''

if __name__ == '__main__':
    
    def druck(l,s):
        if l > 0:
            print l,'x',s
            return druck(l-1,s*l)
        else:
            return 0,'x',s
    
    rest = druck(4,"Mauzi")
    print rest[0],rest[1],rest[2]
    