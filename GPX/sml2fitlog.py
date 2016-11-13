# encoding utf8

# ----------------------------------------------------------------

# stdlib
import argparse
import os

# others

# mines
from work_funcs import identify_files, gather_activities, save_as_fitlog

# ----------------------------------------------------------------

argparser = argparse.ArgumentParser(description="conversion *.sml -> *.fitlog")

grp = argparser.add_argument_group("input")
grp.add_argument('smlfiles', type=str, nargs='+', help='fichiers sml à traiter')
grp.add_argument('--after', type=str, default="2016-07-01", help='sélectionne les fichiers de date supérieure à --after')
grp.add_argument('--before', type=str, default="2019-12-31", help='sélectionne les fichiers de date inférieure à --before')
grp.add_argument('-w', '--workdir', type=str, default=".", help='définit le répertoire de travail')

grp = argparser.add_argument_group("output")
grp.add_argument("-o", "--output", help="fichier fitlog à écrire", type=str, default=None)   # pas d'output = pas de fichier
# TODO : option sur les équipements ?

grp = argparser.add_argument_group("options")
grp.add_argument("--head", help="infos principales uniquement", action='store_true', default=False)
grp.add_argument("-q", "--quiet", help="mode silencieux", action='store_true', default=False)
grp.add_argument("-l", "--list", help="liste uniquement les fichiers à traiter", action='store_true', default=False)

args = argparser.parse_args()

# ----------------------------------------------------------------
#%% goto workdir

initdir = os.getcwd()
os.chdir(args.workdir)

# ----------------------------------------------------------------
#%% gestion de la liste des fichiers

# application des filtres
found_files = identify_files(args.smlfiles, args.after, args.before, args.quiet)
    
# ----------------------------------------------------------------
#%% collection des activités
    
if not args.list:
    def_activities = gather_activities(found_files, args.head, args.quiet)
    
# ----------------------------------------------------------------
#%% sortie
        
if args.output and not args.list:
    save_as_fitlog(def_activities, args.output)

