#!python
# -*- coding: iso-8859-15 -*-

from Tools import temps_2_heures, heures_2_temps

class Perf:

    def __init__(self, course = None, coureur = None, temps = "", scratch = "", cat = "", dist = None, prive = False, debug = False):
        if cat == None: cat = ""
        if scratch == None: scratch = ""

        self.course = course
        self.coureur = coureur
        self.dist = dist
        self.temps = temps
        self.heures = temps_2_heures(self.temps)
        self.scratch = scratch
        self.cat = cat
        self.prive = prive
        if self.heures <= 0:
            self.vitesse = 0
            self.points = 0
            raise ValueError(str(self))
        self.vitesse = course.dist / self.heures
        self.pace = heures_2_temps(self.heures / course.dist)
        #if self.heures > 8: debug = True
        self.points = self.calcul_points(debug=debug)

    def __repr__(self):
        deniv = ""
        if self.course.deniv > 0:
            deniv = " / %d m+" % self.course.deniv
        dist = self.dist
        if dist == None:
            dist = self.course.dist

        divers = []
        divers.append("%s/km" % self.pace)
        if self.scratch != "":
            divers.append("{self.scratch} ème au scratch".format(self=self))
        if self.cat != "":
            divers.append("{self.cat} ème / cat.".format(self=self))
        #divers.append("{self.vitesse:.1f} km/h".format(self=self))
        return "{self.coureur.prenom} {self.coureur.nom} à {self.course.nom} ({self.course.tag}) - {dist} km{deniv} en {self.temps} ({divers})".format(self=self, deniv=deniv, dist=dist, divers=", ".join(divers))

    def bilan(self):
        deniv = ""
        if self.course.deniv > 0:
            deniv = " / %d m+" % self.course.deniv
        dist = self.dist
        if dist == None:
            dist = self.course.dist

        divers = []
        classt = ""
        import re
        reVictoire = re.compile(r'^([1])\b')
        rePodium = re.compile(r'^([123])\b')
        reEme = re.compile(r'[eè]me')
        if self.scratch != "":
            pod = ""
            if reVictoire.match(self.scratch):
                pod = " : VICTOIRE !"
            elif rePodium.match(self.scratch):
                pod = " : PODIUM !"
            eme = " ème"
            if reEme.search(self.scratch):
                eme = ""
            divers.append("{self.scratch}{eme} au scratch{pod}".format(self=self, pod=pod, eme=eme))
        if self.cat != "":
            pod = ""
            if reVictoire.match(self.cat) and not rePodium.match(self.scratch):
                pod = " : VICTOIRE !"
            elif rePodium.match(self.cat) and not rePodium.match(self.scratch):
                pod = " : PODIUM !"
            eme = " ème"
            if reEme.search(self.cat):
                eme = ""
            divers.append("{self.cat}{eme} {self.coureur.cat}{pod}".format(self=self, pod=pod, eme=eme))
        #divers.append("{self.vitesse:.1f} km/h".format(self=self))
        if len(divers) > 0:
            divers = " (%s)" % ", ".join(divers)
        else:
            divers = ""
        if self.prive:
            if self.coureur.sexe == "F":
                return "une coureuse anonyme était là"
            return "un coureur anonyme était là"
        return "{self.coureur.alias} {self.coureur.nom} : {self.temps}{divers}".format(self=self, deniv=deniv, dist=dist, divers=divers)


    def calcul_points(self, debug = False):

        if debug: print( "\n%s" % self)
        from math import pow

        #try:

        # caracs de la course
        dist = None
        if dist == None:
            dist = self.course.difficulte()
        if 'orient' in self.course.tag:
            dist *= 1.5
        if 'noctu' in self.course.tag:
            dist *= 1.15
        if 'neige' in self.course.tag:
            dist *= 1.15
        if debug: print( " -> dist = %g" % dist)
        vitesseCourse = dist / self.heures
        if debug: print( " -> vitesseCourse = %g" % vitesseCourse)

        # 1er coef
        kAge = self.coureur.k3
        if debug: print( " -> kAge(cat) = %g" % kAge)

        # coef intermédiaire : joue sur kVitesseRef et kDifficulte
        if self.coureur.sexe == 'F':
            from math import log
            kSexe = 0.0538 * log(dist) + 1.0787
        else:
            kSexe = 1.
        if debug: print( " -> kSexe(sexe, dist) = %g" % kSexe)

        # coef vitesse de référence
        kVitesseRef = (0.0001 * pow(dist, 2) - 0.0372 * dist + 10.294) / kSexe
        if debug: print( " -> kVitesseRef(dist, kSexe) = %g" % kVitesseRef)

        # coef difficulté
        if dist < 10.01:
            kDifficulte = 7.9616
        elif dist > 103:
            kDifficulte = 32.61
        else:
            kDifficulte = -0.00000003 * pow(dist, 5) + 0.00001003 * pow(dist, 4) - 0.001215 * pow(dist, 3) + 0.06 * pow(dist, 2) - 0.65 * dist + 9.5793
        if debug: print( " -> kDifficulte(dist) = %g" % kDifficulte)

        if debug: print( " -> h  = %g" % self.heures)

        # ok
        pointcourse = (kAge * vitesseCourse - kVitesseRef) * kDifficulte * kSexe
        if debug: print( "  = points = %.1f" % pointcourse)
        pointcourse = max(1, pointcourse)
        self.points = pointcourse

        #except Exception as ex:
        #print( "erreur dans le calcul des points de " + str(self))
            #raise ex

        return self.points

# ----------------

class ParticipationNonDocumentee(Perf):

    def __init__(self, course = None, coureur = None, descr = None):
        self.course = course
        self.coureur = coureur
        self.descr = descr
        self.deniv = ""
        self.temps = '01:23:45' # pour les tris, je ne mets pas 0. ni 99. car cela perturbe l'analyse des min/max
        self.heures = temps_2_heures(self.temps)
        if self.course.deniv > 0:
            self.deniv = " / %d m+" % self.course.deniv
        self.points = 0
        self.scratch = ''
        self.cat = ''
        self.vitesse = 0

    def __repr__(self):
        return "{self.course.nom} - {self.course.dist} km{self.deniv} : {self.descr}".format(self=self)

    def bilan(self):
        return "{self.descr}".format(self=self)

    def calcul_points(self, debug = False):
        return self.points

# ----------------

class Abandon(Perf):

    def __repr__(self):
        deniv = ""
        if self.course.deniv > 0:
            deniv = " / %d m+" % self.course.deniv
        return "{self.coureur.prenom} {self.coureur.nom} à {self.course.nom} - {self.course.dist} km{deniv} : ABANDON après {self.temps}".format(self=self, deniv=deniv)

    def calcul_points(self, debug = False):
        self.points = 1
        return self.points
