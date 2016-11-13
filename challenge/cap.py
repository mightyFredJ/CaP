#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from Coureur import *
from Course import *
from Init import *
from Tools import *

from sys import argv
print(" ".join(argv))

# ----------------------------------------------------------------
# options

import argparse
parser = argparse.ArgumentParser(description="""Collecte & Analyse des perfs ; pré-requis : fichier 'coureurs.csv' dans le répertoire""")

group = parser.add_argument_group("saisie des donnees d'entrée")
parser.add_argument("fichier_resu", help="listing de résultats", nargs="*")

group = parser.add_argument_group("analyse")
parser.add_argument("-i", "--inspect",  help="details de coureurs",     action="append", default=list(), metavar='COUREUR')
parser.add_argument("-s", "--stats",    help="liste de toutes les perfs", action="store_true", default=False)
parser.add_argument("-b", "--bilan",    help="bilan des courses",   action="store_true", default=False)
parser.add_argument("-c", "--classt",   help="classement final",    action="store_true", default=False)
parser.add_argument("-g", "--graph",    help="nuage pnts=f(diff)",  action="store_true", default=False)
parser.add_argument("-a", "--annee",    help="faits marquants de l'année", action="store_true", default=False)
parser.add_argument(      "--geo",      help="carte de France",  action="store_true", default=False)
parser.add_argument(      "--histo",    help="histogrammes",  action="store_true", default=False)

group = parser.add_argument_group("options")
parser.add_argument("-d", "--debug", help="suivi des traitements", action="store_true", default=False)
parser.add_argument("-q", "--quiet", help="désactive les avertissements lors de la lecture", action="store_true", default=False)
parser.add_argument(      "--max",   help="nb max de courses attribuant des points", type=int, default=8)
parser.add_argument("-t", "--short", help="listes réduites à STOP éléments", type=int, metavar='STOP', default=10000)
parser.add_argument("-z", "--zero",  help="PAS d'arrêt des listes à zéro", action="store_true", default=False)
parser.add_argument(      "--camemb", help="camemberts", action="store_true", default=False)
parser.add_argument(      "--calend", help="calendrier", action="store_true", default=False)

args = parser.parse_args()
if len(args.fichier_resu) == 0:
	parser.print_help()
	exit()

# gestion manuelle des globs
fichiers_a_lire = []
import os.path
import re
import glob
for fichier in args.fichier_resu:
    if not os.path.exists(fichier) and re.search(r'[\*\?]', fichier):
        fichiers_a_lire.extend(glob.glob(fichier))
    else:
        fichiers_a_lire.append(fichier)
#print("%d fichiers à lire : [%s]" % (len(fichiers_a_lire), fichiers_a_lire))
args.fichier_resu = fichiers_a_lire

# ----------------------------------------------------------------
# chargement & calculs

if args.quiet:
    import StringIO
    sys.stdout = StringIO.StringIO()

coureurs = loadCoureurs(suivi=args.debug)

# lecture des fichiers
for fichier in args.fichier_resu:
    courses, perfs = loadResults(fichier, coureurs, suivi=args.debug)

if args.quiet:
    sys.stdout = sys.__stdout__

print("%d courses lues (%d perfs)\n" % (len(courses), len(perfs)))

for c in coureurs:
     c.stats(pond = False, nb_max_perfs = args.max)

# ----------------------------------------------------------------
# liste des perfs & géo etc

from pprint import pprint as pp
#pp(perfs)
if args.stats:
    stats(perfs, "tous", geo=False, pond=False, nb_max_perfs = args.max)

if args.geo:
    geographie(perfs)

if args.bilan:
    print()
    print("Détail des", len(courses), "courses :\n")
    for i, c in enumerate(sorted(courses, key=lambda a: a.date)):
        if i+1 > args.short: break
        print(c.bilan())

# ----------------------------------------------------------------
# analyse

for pattern in args.inspect:
    for coureur in [c for c in coureurs if re.search(pattern, c.nom, re.I)]:
        coureur.stats(suivi = True, nb_max_perfs = args.max, pond=False)

# ----------------------------------------------------------------
# classement final

from copy import deepcopy
coureurs.sort(key=lambda a: a.pts_tot, reverse=True)
classt = deepcopy(coureurs)

if args.classt:
    print("\nclassement")
    print()
    print("{:>2s} {:<30s} {:>6s} {:>2s} {:>4s} {:>4s}".format("n", "nom", "points", "nb", "km", "h"))
    for i, c in enumerate(coureurs):
        if i+1 > args.short: break
        if not args.zero and classt[i].pts_tot == 0: break
        print("{:>2d} {:<30s} {:>6.1f} {:>2d} {:>4.0f} {:>4.0f}".format(i+1, classt[i].bilan(), classt[i].pts_tot, len(classt[i].perfs), classt[i].dist_tot, classt[i].tps_tot) ),

# ----------------------------------------------------------------
# nuage pnts = f(nb courses)

if args.graph:
    print()

    from pylab import *
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(111)
    #ax.set_yscale('log')   marche pas ? pourtant le code est repris d'un script qui fonctionne ?

    for crs in courses:
        cloud = []

        print(crs)
        for perf in crs.perfs:
            cloud.append([crs.difficulte(), perf.points, crs.nom])
        #for c in coureurs:
            #cloud.append([len(c.perfs), c.pts_tot, c.nom])

        if len(cloud) == 0:
            continue
        diff, pnt, nom = zip(*cloud)

        import random
        import matplotlib.lines as lines
        from pylab import rand
        color = rand(3)
        marker=random.choice(list(lines.Line2D.markers.keys()))
        ax.plot(diff, pnt, color=color, marker=marker, linestyle='')

        #for c in cloud:
            #x, y, nom = c[0:3]
            #ax.annotate(nom, xy=(x, y),  xycoords='data',
                        #xytext=(5, 5), textcoords='offset points',
                        #arrowprops=dict(arrowstyle="->"),
                        #color=color,
                        #)

    ax.autoscale_view()
    plt.title('pnts = f(diff)')
    plt.show()

# ----------------------------------------------------------------
# FM de l'année

if args.annee:
    print("\nfaits marquants de l'année\n")

    print("%d courses totalisant %d participations" % (len(courses), sum( [len(c.perfs) for c in courses] )))
    kms = sum( [c.dist * len(c.perfs) for c in courses] )
    deniv = sum( [c.deniv * len(c.perfs) for c in courses] )
    hrs = sum( [ sum([p.heures for p in c.perfs]) for c in courses] )
    print("%d kms / %d D+ en %d heures" % (kms, deniv, hrs))
    print()

    print("Nb de podiums :")
    print("  tot : %d places" % (sum( [cr.pods[0] for cr in coureurs] )))
    for place in range(1, 4):
        print("  %d  : %d places" % (place, sum( [cr.pods[place] for cr in coureurs] )))
    print("Nb de podiums par catégorie :")
    print("  tot : %d places" % (sum( [cr.pods_cat[0] for cr in coureurs] )))
    for place in range(1, 4):
        print("  %d  : %d places" % (place, sum( [cr.pods_cat[place] for cr in coureurs] )))
    for cr in coureurs:
        if cr.pods_cat[0] > 0:
            print(cr.nom, ':', cr.pods_cat[0], 'podiums :', cr.pods_cat[1:4])
    
    print()
    coureurs.sort(key=lambda a: len(a.perfs))
    print("Nb de participations par coureur E [%d, %d]" % (len(coureurs[0].perfs), len(coureurs[-1].perfs)))

    coureurs.sort(key=lambda a: a.pods_cat[0])
    print("Nb de podiums par coureur E [%d, %d]" % (coureurs[0].pods_cat[0], coureurs[-1].pods_cat[0]))

    coureurs.sort(key=lambda a: a.dist_tot)
    print("Nb de km par coureur E [%d, %d]" % (coureurs[0].dist_tot, coureurs[-1].dist_tot))

    coureurs.sort(key=lambda a: a.deniv_tot)
    print("D+ par coureur E [%d, %d]" % (coureurs[0].deniv_tot, coureurs[-1].deniv_tot))

    coureurs.sort(key=lambda a: a.tps_tot)
    print("Temps de course par coureur E [%d, %d]" % (coureurs[0].tps_tot, coureurs[-1].tps_tot))


    print()
    courses.sort(key=lambda a: a.dist)
    print("Distances des courses E [%.1f, %.1f]" % (courses[0].dist, courses[-1].dist))
#    for c in courses[-10:()]:
#        print(c.dist, c)

    courses.sort(key=lambda a: a.deniv)
    print("Dénivelés des courses E [%d, %d]" % (courses[0].deniv, courses[-1].deniv))
    # for c in courses[0:10]:
        # print c.deniv, 'm+ pour', c, '(%d participants)' % len(c.perfs)

    # courses.sort(lambda a, b: cmp(b.deniv*len(b.perfs), a.deniv*len(a.perfs)))
    # print "Dénivelés cumulé des courses E [%d, %d]" % (courses[0].deniv * len(courses[0].perfs), courses[-1].deniv * len(courses[-1].perfs))
    # for c in courses[0:20]:
        # print c.deniv*len(c.perfs), 'm+ pour', c, '(%d participants)' % len(c.perfs)

    courses.sort(key=lambda a: len(a.perfs))
    print("Nb de participants par course E [%d, %d]" % (len(courses[0].perfs), len(courses[-1].perfs)))


    print()
    perfs.sort(key=lambda a: a.heures)
    print("Temps max sur une course E [%s, %s]" % (perfs[0].temps, perfs[-1].temps))
#    for p in perfs:
#        print p.temps, p

    perfs.sort(key=lambda a: a.points)
    print("Points max sur une course E [%d, %d]" % (perfs[0].points, perfs[-1].points))

    perfs.sort(key=lambda a: a.vitesse)
    print("Vitesse max sur une course E [%.1f, %.1f]" % (perfs[0].vitesse, perfs[-1].vitesse))
    #for p in perfs:
        #print p.vitesse, p

# ----------------------------------------------------------------
# autres sorties

if args.camemb:
    from graphiques import camemberts
    camemberts(courses)

if args.histo:
    from graphiques import histogrammes
    histogrammes(courses)

if args.calend:
    from graphiques import calendrier
    calendrier(courses, what='dist', ylabel='kms cumulés')
