#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import os.path
import sys
import re

# ----------------------------------------------------------------

# TODO : les appels à subprocess fait perdre environ 0.3 sec !
def hgrev(texte):
    """    $ hg log --template '{rev}' -r tip
           2
    """
    import subprocess
    rev = subprocess.check_output("hg log --template '{rev}' -r tip")
    return rev[1:-1]    # sinon on récupère des guillemets simples
 
def hgdate(texte):
    """    $ hg log --template '{date|isodate}' -r tip
           2015-04-14 17:16 +0200
    """
    import subprocess
    date = subprocess.check_output("hg log --template '{date|isodate}' -r tip")
    import re
    date = re.sub(r' [-+]\d{4}$', '', date[1:-1])
    return date

# ----------------------------------------------------------------

def today(sep = "/"):
    format = "".join(["%d", sep, "%m", sep, "%Y"])
    import datetime
    return datetime.date.today().strftime(format)

def now(sep = ":"):
    format = "".join(["%H", sep, "%M", sep, "%S"])
    import time
    return time.strftime(format, time.localtime())

def welcome(prog = "", message = ""):
    descr = ""
    if 'VERSION' in sys.modules['__main__'].__dict__:
        descr += "v%s " % sys.modules['__main__'].__dict__['VERSION']
    if 'DATE' in sys.modules['__main__'].__dict__:
        descr += "(%s) " % sys.modules['__main__'].__dict__['DATE']
    
    cwd = os.getcwd()
    progpath = os.path.dirname(prog)
    # fait chier, dans Eclipse le chemin de l'exe apparaît toujours, ça pollue ma sortie
    if cwd == progpath:
        prog = os.path.basename(prog)
        sys.argv[0] = prog
    
    retour = Titre("%s\n    %s %s" % (message, prog, descr.strip())) + "\n"
    retour += "Traitement effectué le %s à %s\n\n" % (today(), now())
    retour += "cd " + os.getcwd() + "\n"
    retour += " ".join(sys.argv) + "\n"
    retour += '\n----------------------\n'
    return retour

# ----------------------------------------------------------------

def Titre(what):
    retour = '\n------------------------------------------------\n' + what + "\n"
    retour += '------------------------------------------------\n'
    return retour

def Paragraphe(what):
    return '\n----------------------\n' + what + "\n"

# ----------------------------------------------------------------

from StringIO import StringIO

class teeStringIO(str):
    
    def __init__(self):
        self.data = ""
        
    def write(self, _buffer):
        sys.__stdout__.write( _buffer )

        try:
            self.data += _buffer
        except UnicodeDecodeError as err:
            sys.stdout = sys.__stdout__  
            print "    PANIC    " * 10
            print
            print err
            print _buffer.__class__
            print "[" + _buffer + "]"
            print len(_buffer)
            print sys.getdefaultencoding()
            
            print
            print err.start
            print " " * err.start + "^"
            print " " * err.start + "|"
            print err.object[err.start:err.end], ":", ord(err.object[err.start:err.end])

            sys.exit(-1)
            
    def getvalue(self):
        return self.data #.encode('utf8')
    
#     
#     
# def capture_stdout(cmd):
#     """ appelle une fonction et capture sa sortie standard
#         renvoie une str
#     """    
#     stdout = StringIO()
#     from options import debug
#     if debug: stdout = teeStringIO()
#     sys.stdout = stdout
#     cmd()
#     sys.stdout = sys.__stdout__
#     return stdout.getvalue()
# 
# def console(msg = "\n"):
#     sys.__stdout__.write(msg)

# ----------------------------------------------------------------

def read_file(filename):
    """ émulation du perl5's File::Slurp qw/slurp/
        renvoie le texte lu
    """
    with open(filename, 'rb') as finp:
        return finp.read()

def write_file(filename, text):
    """ émulation du perl5's File::Slurp qw/read_line/
        pas de valeur de retour ; pas de gestion des exceptions
    """
    with open(filename, 'wb') as fout:
        fout.write( text )

# ----------------------------------------------------------------
