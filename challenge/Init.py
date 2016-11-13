#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from Coureur import *
from Course import *
from Perf import *

import re
import sys

courses = list()
perfs = list()

# ----------------

def loadResults(nomfichier, coureurs, suivi = False):
    print("\nsaisie des résultats de", nomfichier)

    global courses
    global perfs

    fRESU = open(nomfichier, 'r')
    for ligne in fRESU:
        ligne = ligne.strip()

        if ligne == "" or ligne.isspace() or ligne.startswith('#'):
            continue

        elif ';' in ligne:  # nouvelle course
            courses.append( loadCourse(ligne, suivi) )
            pass

        else:               # coureur
            perf = loadPerf(ligne, coureurs, courses[-1], suivi)
            if perf != None:
                perfs.append( perf )
            pass

    fRESU.close()
    return courses, perfs

# ----------------

def loadCoureurs(suivi = False):

    print("\nsaisie des coureurs")

    def_coureurs = open("coureurs.csv", "r")

    coureurs = list()

#ADAM;Erwan;V1H
#ALLARD;Jérôme;SH
    for coureur in def_coureurs:
        datas = [a for a in coureur.split(';')]# if not re.match(r'^\s*$', a)]
        datas = [c.strip() for c in datas]
        if len(datas) == 4:
            nom, prenom, cat, alias = datas
            regSexe = re.match(r'[JSV] \d* ([HF])', cat, re.X)
            if regSexe:
                sexe = regSexe.group(1)
            else:
                raise ValueError('Sexe introuvable dans "%s" pour %s' % (cat, coureur))

        # ajout dans la base
            coureurs.append( Coureur(nom=nom, prenom=prenom, cat=cat, sexe=sexe, alias=alias) )#, age=2013-int(annee)) )
            if suivi: print(coureurs[-1])
        else:
            if coureur != "\n":
                print("ligne '{}' ignorée".format(coureur[0:-1]))

    return coureurs

# ----------------

def loadCourse(ligne, suivi = False):

    if suivi:
        print("\ncourse [%s]" % ligne)

    datas = [c.strip() for c in ligne.split(';')]
    cout = "0 0"
    desc = ""
    course = None
    if len(datas) == 8:
#        cout = datas.pop()
        desc = datas.pop()
    if len(datas) == 7:
        nom, ville, depart, date, dist, deniv, tag = datas
        #if not re.match(r'^\d+$', deniv): deniv = 0
        tag = tag.replace('\n', "")

    # ajout dans la base
        if re.match('\d+h', dist):
            course = CourseHoraire(nom=nom, lieu=ville, depart=depart, date=date, duree=dist, deniv=deniv, tag=tag, cout=cout, desc=desc)
        else:
            course = Course(nom=nom, lieu=ville, depart=depart, date=date, dist=dist, deniv=deniv, tag=tag, cout=cout, desc=desc)
        if suivi: print("   ", course)
    else:
        print("ligne '{}' ignorée".format(ligne.replace('\n', '')))

    return course

# ----------------

def loadPerf(ligne, coureurs, pcourse, suivi = False):

    if suivi:
        print("perf [%s]" % ligne)

#BORDAS 0:48:46 1162ème/10276 98ème/660
#DUMOUCHEL 0:52:59 2010ème/10276 29ème/637
#DEVILLE           NO_ENDORPHINE
#BERARD 0:55:31 94/149 5/25
#DAUVERGNE Emmanuelle 01:08:27
#JASSERAND 3:50:06 20 62

    import re
    regPerf = re.compile(r'^(?P<coureur> .* ) \s+ (?P<temps> (?: \d+[h:°] )? (?: \d+[m:\'] ) (?: \d+[s\']* )? ) \s* (?P<scratch> \S+ )? \s* (?P<cat> \S+ )? \s* (?P<prive> NO_ENDORPHINE)?', re.X | re.I)
    matcher = regPerf.match(ligne)
    perf = None
    pcoureur = None

    def normaliseNom(nom):
        nom = nom.lower()
        nom = re.sub('[éèë]', 'e', nom)
        nom = re.sub('[ôö]', 'o', nom)
        nom = re.sub('[àâä]', 'a', nom)
        nom = re.sub('ç', ' c', nom)
        #nom = re.sub('[ï]', 'i', nom)
        #nom = re.sub('[ùû]', 'u', nom)
        return nom

    if re.search(r'".*"', ligne):
        perf = ParticipationNonDocumentee(course = pcourse, descr = ligne.replace(r'"', ''))
        pcourse.perfs.append(perf)

    elif matcher != None:
        nomcoureur = normaliseNom( matcher.group('coureur').strip() )
        temps = matcher.group('temps')
        scratch = matcher.group('scratch')
        cat = matcher.group('cat')
        prive = matcher.group('prive')
        if scratch == "NO_ENDORPHINE":
            scratch = ""
            prive = "NO_ENDORPHINE"
        if cat == "NO_ENDORPHINE":
            cat = ""
            prive = "NO_ENDORPHINE"
        prive = prive == "NO_ENDORPHINE"
        if suivi: print("    identifié [%s, %s, %s, %s, %s]" % (nomcoureur, temps, scratch, cat, prive))

    # recherche du coureur correspondant
        #for coureur in coureurs:
            #if nomcoureur == "{} {}".format(coureur.nom, coureur.prenom):
                #pcoureur = coureur
                #break
        mots = nomcoureur.lower().split()
        for coureur in coureurs:
            nom = normaliseNom( "{} {}".format(coureur.nom, coureur.prenom) )
            cpt = 0
            for mot in mots:
                # print("            %s in %s = %s" % (mot, nom, mot in nom))
                if mot in nom:
                    cpt += 1
            # print("       vs %s : %d/%d pts" % (nom, cpt, len(mots)))
            if cpt == len(mots):
                pcoureur = coureur
                break

        if pcourse != None and pcoureur != None:
            perf = Perf(course=pcourse, coureur=pcoureur, temps=temps, scratch=scratch, cat=cat, prive=prive)    # je ne gère pas les courses horaires
            if scratch == "ABD":
                perf = Abandon(course=cs, coureur=cr, temps=temps, scratch=scratch, cat=cat)

            if suivi: print("   ", perf)
            pcourse.perfs.append(perf)
            pcoureur.perfs.append(perf)

        else:
            print("ligne '{}' ignorée (course {} coureur {})".format(ligne, pcourse, pcoureur))

    else:
        print("ligne '{}' ignorée (course {})".format(ligne, pcourse))

    return perf
