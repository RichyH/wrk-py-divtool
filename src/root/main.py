#!/usr/bin/env python
# coding=UTF-8
'''
Created on 21.02.2013

@author: Richy Hareter, Last Backup function and the mighty sed command by Zoltan Szöke
'''
import os
import re
import shutil
import subprocess
import sys
from stat import S_IRUSR,S_IWUSR,S_IXUSR,S_IRGRP,S_IXGRP,S_IROTH,S_IXOTH

if __name__ == '__main__':
#-------------------------------------------------------------------------------------------------------------------------------------
    def dirno(item): 
        return item[1]
    def recno(item):
        return item[0]
    def divtype(item):
        return item[2]
    def additems(searchresult,divtype):
        for fields in searchresult:
            if fields.group(2) is not None:
                items.append(())
                if (divtype != divType['Dir'] and divtype != divType['Ics']):
                    items[len(items)-1] = (len(items),fields.group(2),fields.group(3),fields.group(4))
                elif divtype == divType['Ics']:
                    items[len(items)-1] = (len(items),fields.group(2),fields.group(3),fields.group(4),fields.group(5))
                else:
                    items[len(items)-1] = (len(items),fields.group(2),fields.group(3))
    
    divType = {'Dir' : 0,'FmeEcf' : 1,'Ics' : 2,'Pen' : 3}
    
    regSearchV4Dir =    re.compile(r'(^(\d+?)\s.*?(DIR))',re.I | re.M)
    regSearchV4FmeEcf = re.compile(r'(^(\d+?)\s.*?(FME|ECF)[\s\S]+?\3\s?=\s?(\d+))',re.I | re.M)
    regSearchV4Ics =    re.compile(r'(^(\d+?)\s.*?(ICS)[\s\S]+?ICS-CODE\s?=\s?(\d+)\s*([\w/ ]*)\s\()',re.I | re.M)#)',re.I | re.M)
    regSearchV4Pen =    re.compile(r'(^(\d+?)\s.*?(PEN)[\s\S]+?LIST\s?=\s?(\d))',re.I | re.M)
    regSearchV5Dir =    re.compile(r'(^DIRECTORY NUMBER):.([0-9]{1,10}).*\n^DIV STATE:.*(DIR),?.*\n',re.I | re.M)
    regSearchV5FmeEcf = re.compile(r'(^DIRECTORY NUMBER):.([0-9]{1,10}).*\n^DIV STATE:.*(FME|ECF),?.*\n^ADD INFO:.*?\3\s?=\s?(\d{1,}),',re.I | re.M)
    regSearchV5Pen =    re.compile(r'(^DIRECTORY NUMBER):.([0-9]{1,10}).*\n^DIV STATE:.*(PEN),?.*\n^ADD INFO:.*LIST\s?=\s?(\d*),?',re.I | re.M)
    regSearchV5Ics =    re.compile(r'(^DIRECTORY NUMBER):.([0-9]{1,10}).*\n^DIV STATE:.*(ICS),?.*\n^ADD INFO:.*ICS-CODE\s?=\s?(\d+)\s*([\w ]*)\s\(',re.I | re.M)
    regSearchV5Cmpl =   re.compile(r'(^DIRECTORY NUMBER):.([0-9]{1,10}).*\n(^DIV STATE):.([A-Z, ]{1,}).*\n(^ADD INFO):.([-=\w(,) ]*)',re.I | re.M)
#-------------------------------------------------------------------------------------------------------------------------------------
    items = []
    if len(sys.argv) == 3:
        try:
            WorkExtn = sys.argv[sys.argv.index('-wd')+1]
        except ValueError:
            sys.exit("Bitte den -wd Parameter angeben. Er soll die Nebenstelle, welche zum Umleiten verwendet wird, enthalten")
    else:
        sys.exit("Bitte den -wd Parameter angeben. Er soll die Nebenstelle, welche zum Umleiten verwendet wird, enthalten")

#-------------------------------------------------------------------------------------------------------------------------------------
    WorkDir = os.getcwd() + '/'
    try:
        output = subprocess.Popen("ls /var/opt/eri_sn/ -t1 |head -n1",stdout=subprocess.PIPE,shell=True).communicate()
        BackupDir =  '/var/opt/eri_sn/' + output[0][:len(output[0])-1] + '/'
        shutil.copyfile(BackupDir+'DED.D',WorkDir+'DED.D.bak')
        SusipCmdFile = open(WorkDir+'SUSIP.cmd','w')
        print >> SusipCmdFile, '#!/bin/bash/'
        SedCmd =  "sed -e '1,138d;s/[ \\t] //g;s/^[\"[]*/mdsh -c susip:dir=/;s/\".*/\\\\;/' " + WorkDir + "DED.D.bak >> " + WorkDir + "SUSIP.cmd"
        subprocess.call(SedCmd,shell=True)
#        subprocess.call("lsof | grep SUSIP.cmd",shell=True)
        os.remove(WorkDir + 'DED.D.bak')
        os.chmod(WorkDir + 'SUSIP.cmd',S_IRUSR|S_IWUSR|S_IXUSR|S_IRGRP|S_IXGRP|S_IROTH|S_IXOTH)
            subprocess.call(WorkDir + "SUSIP.cmd > " + WorkDir + "SUSIP.log",shell=True)
    except: sys.exit("Fehler beim Erstellen von SUSIP.log!")
#-------------------------------------------------------------------------------------------------------------------------------------
    SusipInputFile = open(WorkDir + 'SUSIP.log','r')
    rawdata = SusipInputFile.read()
    SusipInputFile.close()
    del SusipInputFile

    additems(regSearchV4Dir.finditer(rawdata),divType['Dir'])
    additems(regSearchV4FmeEcf.finditer(rawdata),divType['FmeEcf'])
    additems(regSearchV4Ics.finditer(rawdata),divType['Ics'])
    additems(regSearchV4Pen.finditer(rawdata),divType['Pen'])
    additems(regSearchV5Dir.finditer(rawdata),divType['Dir'])
    additems(regSearchV5FmeEcf.finditer(rawdata),divType['FmeEcf'])
    additems(regSearchV5Ics.finditer(rawdata),divType['Ics'])
    additems(regSearchV5Pen.finditer(rawdata),divType['Pen'])
        
    items.sort(key=dirno)
    
    OutputFilePath = WorkDir + 'RecreateDiv.cmd'
    SusipOutputFile = open(OutputFilePath,'w')
    
    print >> SusipOutputFile, '#!/bin/bash'
    for item in items:
#        if item[2] == 'DIR':
#            print >> SusipInputFile, """/opt/eri_sn/bin/mdsh -c 'extension_procedure -d """ + WorkExtn + ' --proc "*21*' + WorkExtn + '*' + item[1] + """#";'"""
#            continue
        if item[2] == 'FME':
            print >> SusipInputFile, """/opt/eri_sn/bin/mdsh -c 'extension_procedure -d """ + WorkExtn + ' --proc "*21*' + item[1] + '*' + item[3] + """#";'""" 
            continue
        if item[2] == 'ECF':
            print >> SusipInputFile, """/opt/eri_sn/bin/mdsh -c 'extension_procedure -d """ + WorkExtn + ' --proc "*22*' + item[1] + '#' + item[3] + """#";'"""
            continue
        if item[2] == 'PEN':
            print >> SusipInputFile, """/opt/eri_sn/bin/mdsh -c 'call_list -d """ + item[1] + ' --list ' + item[3] + """;'"""
            continue
        if item[2] == 'ICS':
            if item[4] == 'RETURN NOT SET':
                print >> SusipInputFile, """/opt/eri_sn/bin/mdsh -c 'extension_procedure -d """ + item[1] + ' --proc "*23*' + item[3] + """#";'"""
            else:
                print >> SusipInputFile, """/opt/eri_sn/bin/mdsh -c 'extension_procedure -d """ + item[1] + ' --proc "*23*' + item[3] + '*' + item[4][13:15] + item[4][10:12] + """#";'"""
                
    SusipOutputFile.close()
    del SusipOutputFile
    os.chmod(WorkDir + 'RecreateDiv.cmd',S_IRUSR|S_IWUSR|S_IXUSR|S_IRGRP|S_IXGRP|S_IROTH|S_IXOTH)   

# DIR    extension_procedure -d <DIR> --proc "*21#"
# FME    extension_procedure -d <wrkdir> --proc "*21*<DIR>*<FME>#"
# ECF    extension_procedure -d <wrkdir> --proc "*22*<DIR>#<ECF>#"
# PEN    call_list -d <DIR> --list <LIST>
# ICS    extension_procedure -d <DIR> --proc "*23*<REASON>*<TILL>#" | "*23*<REASON>#"

