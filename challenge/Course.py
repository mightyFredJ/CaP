#!python
# -*- coding: ISO-8859-15 -*-

import re

class Course:

    def __init__(self, nom = "", dist = 0, deniv = 0, lieu = "", depart = "", date = "", cout = "0 0", tag = "", desc = ""):
        self.nom = nom
        dist = re.sub(r'\s*km', '', str(dist))
        self.dist = float(dist)
        deniv = re.sub(r'\s*m\+', '', str(deniv))
        self.deniv = int(deniv)
        self.difficulte()

        self.lieu = lieu
        self.depart = depart
        import datetime
        date = date.replace('/20', '/')
        self.date = datetime.datetime.strptime(date, "%d/%m/%y")

        temp = cout.split()
        euros, subvention = "0", "0"
        if len(temp) > 0: euros = temp[0]
        if len(temp) > 1: subvention = temp[1]
        euros = re.sub(r'\s*€', '', str(euros))
        subvention = re.sub(r'\s*%', '', str(subvention))
        self.cout = float(euros), float(subvention)/100.

        self.perfs = []

        self.tag = tag  # interlabo, cross, trail, nature, route, ultra
        self.desc = desc


    def __repr__(self):
        retour = "{self.nom} ({self.tag}) à {self.lieu} ({self.depart}) le {date}".format(self=self, date=self.date.strftime("%d/%m/%y"))
        if self.desc != "":
            retour += "    " + self.desc
        return retour

    def detail(self):
        return "{self} : {self.dist:.3f} km / {self.deniv:d} m+ (soit une difficulté de {self.diff:.3f})".format(self=self)

    def bilan(self):
        s = ""
        if len(self.perfs) > 1: s = "s"
        deniv = ""
        if self.deniv > 0: deniv = " / {self.deniv:d} m+".format(self=self)
        desc = ""
        if self.desc: desc = "    " + self.desc + "\n"
        txt = """{self.nom} à {self.lieu} ({self.depart}) le {date} :
    course {self.tag} de {self.dist:.3g} km{deniv}
{desc}    {nb} participant{s} :
""".format(
            self=self, nb=len(self.perfs), deniv=deniv, desc=desc, s=s, date=self.date.strftime("%d/%m/%y"))

        from Tools import temps_2_heures
        for p in self.perfs: #sorted(self.perfs, cmp=lambda a, b: cmp(temps_2_heures(a.temps), temps_2_heures(b.temps))):
            txt += "        %s\n" % p.bilan()
        return txt

    def difficulte(self):
        if not 'diff' in dir(self) or self.diff <= 0.:
            self.diff = self.dist + self.deniv / 100.
        return self.diff



class CourseHoraire(Course):

    def __init__(self, nom = "", dist = "", deniv = "", duree = "", lieu = "", depart = "", date = "", cout = "0 0", tag = ""):
        self.duree = duree
        self.iduree = int( duree.replace("h", "") )
        Course.__init__(self, dist = -1, deniv = -1, lieu=lieu, depart=depart, date=date, cout=cout, tag=tag, nom=nom)

    def __repr__(self):
        return "{self.nom} à {self.lieu} ({self.depart}) le {date}".format(self=self, date=self.date.strftime("%d/%m/%y"))

    def detail(self):
        return "{self} : course horaire ({self.duree} h)".format(self=self)

    def difficulte(self):
        if self.iduree == 6:
            self.diff = 60
        elif self.iduree == 12:
            self.diff = 90
        elif self.iduree == 24:
            self.diff = 135
        else:
            print("ATTENTION : difficulté de la course horaire %s définie à 1" % self.nom)
            self.diff = 1
        return self.diff
