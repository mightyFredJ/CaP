#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# définition des arguments principaux
from sys import argv
nbargs = len(argv)
argv.extend( "-c --max 0 -i JASS --short 15 --quiet".split() )

# conteneur des classements par coureur
classements = dict()    # { coureur: { max: classt } }
ensemble_test = range(3, 14, 1)
# ensemble_test = range(1, 6, 1)

# on appelle le programme principal en modifiant le nb de courses prises en compte
# et au passage on stocke les classements des coureurs
for nbcourses in ensemble_test:
    # print argv
    try:
        argv[nbargs+2] = str(nbcourses)
        execfile('cap.py')

        for i, c in enumerate(classt):
            nom = c.bilan()
            if not c.bilan() in classements.keys(): classements[nom] = dict()
            classements[nom][nbcourses] = i
    except:
        pass

# affichage du résultat

# from pprint import pprint as pp
# pp( classements )

# en-tête
print
print "%20s" % "nb courses max =",
for nbcourses in ensemble_test:
    print " %3d" % (nbcourses),
print

# tableau des premiers coureurs (classés selon la dernière valeur de --max considérée)
for i, c in enumerate(classt):
    coureur = c.bilan()
    if i+1 > 20: break
    print "%-20s" % coureur,
    for nbcourses in ensemble_test:
        n = -2
        if nbcourses in classements[coureur]: n = classements[coureur][nbcourses]
        print " %3d" % (n+1),
    print

