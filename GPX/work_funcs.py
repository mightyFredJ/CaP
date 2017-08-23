# encoding utf8

# ----------------------------------------------------------------

# stdlib
import os
import re
from datetime import datetime
import glob
from pathlib import Path
import xml.dom.minidom

# others

# mines
from Activity import Activity
from smlutils import txt_fitlog

# ----------------------------------------------------------------

def identify_files(smlfiles=[], after='', before='', quiet=False):
    """ applique les différents globs et filtres pour lister les fichiers à traiter """
    
    found_files = []
    
    try:

        # glob
        globbed_files = []
        for smlfile in smlfiles:
            globbed_files.extend(glob.glob(smlfile))
        # if len(smlfiles) == 1 and '*' in smlfiles[0]:
            # print('globbing %s...' % smlfiles[0])
            # smlfiles = glob.glob(smlfiles[0])

        # définition des filtres sur les dates
        after_date = datetime.strptime(after, '%Y-%m-%d')
        before_date = datetime.strptime(before, '%Y-%m-%d')
        def filtre_date(filename):
            " 32E9195109001A00-2016-08-14T17_56_25-0 "
            file_date_str = re.search(r'(\d+-\d+-\d+)T', str(filename)).group(1)
            file_date = datetime.strptime(file_date_str, '%Y-%m-%d')
            return after_date <= file_date and file_date <= before_date 	# True <=> le fichier valide la condition

        # application des filtres
        found_files = []
        for filename in globbed_files:
            smlfile = Path(filename)
            if not filtre_date(smlfile):
                if quiet:
                    pass
                else:
                    print('(%s est éliminé par sa date)' % (smlfile.name))
                continue

            print(smlfile.name)
            found_files.append(smlfile)
            
        count = len(found_files)
        s = "s" if count > 1 else ""
        print('{count} fichier{s} identifié{s}\n'.format(**locals()))
        
    except BaseException as ex:
        print('echec lors de la recherche des fichiers : %s' % (str(ex)))
        found_files = []
        # raise ex
    finally:
        pass
        
    return found_files

# ----------------------------------------------------------------

def gather_activities(smlfiles=[], head=False, quiet=False, ui=None,
                      do_guess_loc=True, do_guess_equ=True,
                      ):
    """ analyse les fichiers sml listés """
    
    def_activities = []
    try:

        for smlfile in smlfiles:
            with smlfile.open() as fsml:
                xmlcontent = fsml.read()    
                xmlroot = xml.dom.minidom.parseString(xmlcontent)
                act = Activity(xmlroot.firstChild.getElementsByTagName('DeviceLog')[0], smlfile.name,
                               do_guess_loc=do_guess_loc, do_guess_equ=do_guess_equ,
                               )
                
                if head:
                    print(act.head())
                elif quiet:
                    pass
                else:
                    print(act)
                def_activities.append(act.getAsFitlogFormat())
                
                if ui != None:
                    ui()
            
        count = len(def_activities)
        s = "s" if count > 1 else ""
        print('{count} activité{s} collectée{s}'.format(**locals()))

    except BaseException as ex:
        print('echec lors de l\'analyse des fichiers : %s' % (str(ex)))
        def_activities = []
        raise ex
    finally:
        pass
        
    return def_activities

# ----------------------------------------------------------------

def save_as_fitlog(activities=[], output="temp.fitlog", quiet=False):
    try:
        with open(output, 'w') as fflog:
            fflog.write( txt_fitlog.format(Activities="\n".join(activities)) )

        count = len(activities)
        s = "s" if count > 1 else ""
        print('{count} activité{s} enregistrée{s} sous {output}'.format(**locals()))

    except BaseException as ex:
        print('echec lors de l\'enregistrement : %s' % (str(ex)))
        def_activities = []
        # raise ex
    finally:
        pass
        
