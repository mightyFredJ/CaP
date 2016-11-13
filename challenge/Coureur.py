#!python
# -*- coding: ISO-8859-15 -*-

class Coureur:

    def __init__(self, nom = "", prenom = "", cat = "", sexe = "", alias = ""):
        self.prenom = prenom
        self.nom = nom
        #self.age = age
        self.cat = cat
        self.sexe = sexe
        self.alias = alias
        if self.alias == "" or self.alias == None:  self.alias = self.prenom
        #import re
        #if re.match(r'^[hm]', sexe, re.I):
            #self.sexe = "H"
        #elif re.match(r'^[f]', sexe, re.I):
            #self.sexe = "F"
        #else:
            #raise ValueError("Impossible d'identifier le sexe dans '{}'".format(sexe))

        self.k3 = 0
        self.categorie()
        self.perfs = []
        self.pods = [0, 0, 0, 0]    # [tot, 1er, 2ème, 3ème]
        self.pods_cat = [0, 0, 0, 0]    # [tot, 1er, 2ème, 3ème]

    def stats(self, suivi = False, pond = True, nb_max_perfs = 1000):
        if not suivi:
            import sys
            import io
            sys.stdout = io.StringIO()

        from Tools import stats
        self.nb, self.tps_tot, self.dist_tot, self.deniv_tot, self.pts_tot, self.pts_pond, self.pods, self.pods_cat = \
            stats(self.perfs, pond=pond, nb_max_perfs = nb_max_perfs, label=self.bilan())

        if not suivi:
            import sys
            sys.stdout = sys.__stdout__

        #self.cout_tot = sum( [p.course.cout for p in self.perfs] )
        #print self.detail()
        #print self.pts_tot


    def __repr__(self):
        return "{self.prenom} {self.nom} ({self.cat})".format(self=self)

    def bilan(self):
        return "{self.alias} {self.nom}".format(self=self)

    def detail(self):
        return "{self.alias} {self.nom} : {self.dist_tot:.1f} km en {self.tps_tot:.1f} h en {self.nb} courses, {self.pods[0]} podiums, {self.pods_cat[0]} par catégorie".format(self=self)

    def categorie(self):
        if "J" in self.cat:
            self.k3 = 1.05
        elif "S" in self.cat:
            self.k3 = 1
        elif "V1" in self.cat:
            self.k3 = 1.05
        elif "V2" in self.cat:
            self.k3 = 1.12
        elif "V3" in self.cat:
            self.k3 = 1.2
        elif "V4" in self.cat:
            self.k3 = 1.35
        else:
            raise ValueError('Aucune catégorie trouvée dans "%s" chez %s %s' % (self.cat, self.nom, self.prenom))

## ----------------

#def cat2age(cat):
    #import re
    #regcat = re.match(r'(J|S|V)([HF])([1234])?', cat)
    #if regcat:
        #cat = regcat.group(1)
        #sexe = regcat.group(2)
        #if regcat.group(3) != None:
            #cat += regcat.group(3)
    #else:
        #raise ValueError("Catégorie '%s' invalide" % cat)
    #if cat == "J":
        #age = 19
    #elif cat == "S":
        #age = 35
    #elif cat == "V1":
        #age = 45
    #elif cat == "V2":
        #age = 55
    #elif cat == "V3":
        #age = 65
    #elif cat == "V4":
        #age = 75
    #else:
        #raise ValueError("Catégorie '%s' invalide" % cat)
    #return age, sexe

# ----------------
