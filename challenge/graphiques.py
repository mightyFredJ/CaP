# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 11:13:07 2015

@author: fj221066
"""

from pylab import *
import matplotlib.pyplot as plt
from pprint import pprint as pp
from collections import Counter

import mycolors
import matplotlib.cm as cm
import matplotlib.colors as colors

# ----------------------------------------------------------------

def camemberts(courses):
    print
    tags = Counter()
    tags_p = Counter()
    mois = Counter()

# on parcourt tous les tags
    for c in courses:
        tt = c.tag.split()
    # on essaie d'en retenir un seul par course
        for tag in tt:
            if tag == "interlabo": tag = 'cross'
            tags[tag] += 1
            tags_p[tag] += len(c.perfs)
            mois[c.date.month] += 1

    pp(tags)

# maintenant je n'ai pas envie de tous les afficher,
#   je ne retiens que ceux qui m'intéressent
    for t in ['KV', 'festif', 'orientation', 'ultra',
              'nocturne', 'étapes', 'neige', 'désert']:
        del tags[t]
        del tags_p[t]
    print("%d tags retenus :" % sum([int(v) for v in tags.values()]))
    pp(tags)

    # make a square figure and axes
    fig = figure(1, figsize=(8,8))
#    ax = axes([0., 0., 1., 0.1])   # inutile ?
    fig.clear()

    cols = {
        'route': 'DarkCyan',
        'trail': 'DarkGreen',
        'nature': 'Chartreuse',
        'cross': 'SaddleBrown',
        'montagne': 'Khaki',
#        'cross': 'Orange',
#        'ultra': 'Red',
#        'neige': 'White',
#        'equipe': 'white',
#        'feminine': 'pink',
#        'orientation': 'yellow',
#        'nocturne': 'aquamarine',
#        'festif': 'purple',
    }

    #subplot(221)
    rcParams['xtick.labelsize'] = 'x-large'
    pie(list(tags.values()), labels=tags.keys(), colors=[cols[c] for c in tags.keys()],
        autopct='%d %%', shadow=True)#, pctdistance=1.3)
#    title('Courses par type', bbox={'facecolor':'0.8', 'pad':5})
    fig.savefig('camemb_courses.png')
    fig.clear()

    #subplot(222)
    def fmt(a):
        #print a, str(tags_p[a])
        return str(tags_p[a])
    pie(list(tags_p.values()), labels=tags_p.keys(), colors=[cols[c] for c in tags_p.keys()], autopct='%1.1f%%', shadow=True)
#    title('Participations par type', bbox={'facecolor':'0.8', 'pad':5})
    fig.savefig('camemb_perfs.png')
    fig.clear()

# ----------------------------------------------------------------

def calendrier(courses, what = 'dist', ylabel = 'kms cumulés'):
    """
        je crée un dict où les clés sont le 1er de chaque mois,
        dans les valeurs on place directement les courses
    """
    from collections import defaultdict
    dicmois = defaultdict(list)
    from datetime import date
    for c in courses:
        j = date(c.date.year, c.date.month, 1)
        dicmois[j].append(c)

    print("\ncalendrier")
    x = []
    y = []

    for mois in sorted(dicmois.keys()):
        courses = dicmois[mois]
        # print('\n', mois, ':')
        # for c in courses:
            # print(c)
        date = mois.strftime("%b %Y")
        nb = len(dicmois[mois])
        kms = int(sum( [getattr(c, what) * len(c.perfs) for c in courses] ))
        # print( "{date} : {nb:2d} courses = {kms:4d} kms".format(**locals()))
        x.append(date[:3])
        y.append(kms)

    x_pos = np.arange(len(x))
    w = 0.8
    bars = plt.bar(x_pos, y, align='center', width=w)
    plt.xticks(x_pos, x)
    plt.xlabel("mois")
    plt.ylabel(ylabel)
    plt.xlim( -0.5, len(x)-0.5)

    # plt.cm.register_cmap(name='cea', data=_coolwarm_cea)
    cmap = plt.get_cmap('Reds')
    fracs = [float(a)/max(y) for a in y]
    norm = colors.Normalize(min(fracs), max(fracs))

    for thisfrac, thispatch in zip(fracs, bars):
        color = cmap(norm(thisfrac))
        thispatch.set_facecolor(color)

#    plt.show()
    plt.savefig('calendrier.png')

# ----------------------------------------------------------------

def histogrammes(courses):
# calcul de l'histogramme
    import numpy as np
    dists = [c.dist for c in courses]
    hist, bins = np.histogram(dists, bins=np.linspace(0, 260, 26+1))#26*2+1))
#    diffs = [c.diff for c in courses]
#    hist, bins = np.histogram(diffs, bins=np.linspace(0, 400, 40))
#    print(hist)
#    print(bins)

# debut du dessin
    width = (bins[1] - bins[0]) * 0.8
    center = (bins[:-1] + bins[1:]) / 2
    rcParams['axes.labelsize'] = 'x-large'
    rcParams['xtick.labelsize'] = 'large'
    rcParams['ytick.labelsize'] = 'large'
    bars = plt.bar(center, hist, align='center', width=width)#, log=True)

# couleurs
    plt.cm.register_cmap(name='cea', data=mycolors._coolwarm_cea)
    cmap = plt.get_cmap('Reds')
    cmap = plt.get_cmap('cea')#coolwarm')#OrRd')#Reds')
    xmoys = [b+bins[1]-bins[0] for b in bins[:-1]]
    norm = colors.Normalize(5, 100)#xmoys[0], xmoys[-1])

    for thisx, thispatch in zip(xmoys, bars):
    # hack : les derniers en noi
        color = cmap(norm(thisx))
        if thisx > 150: color = 'k'
        thispatch.set_facecolor(color)

# finalisation
    plt.xlabel("distance (km)")
    plt.ylabel("nombre de courses")
    plt.xlim(0, 120)
    plt.savefig('histogramme.png')
