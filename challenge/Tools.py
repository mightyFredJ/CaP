#!python
# -*- coding: iso-8859-15 -*-

from Coureur import *
from Course import *

import matplotlib.pyplot as plt
import numpy as np

import mycolors
import matplotlib.cm as cm
import matplotlib.colors as colors

# ----------------------------------------------------------------

def temps_2_heures(tps):
    import re

    matcher = re.match(r'(\d+) [hH:°] (\d+) [mM:\'] (\d+) [sS\']*', tps, re.X)
    if matcher != None:
        return float(matcher.group(1)) + float(matcher.group(2))/60. + float(matcher.group(3))/3600.

    matcher = re.match(r'             (\d+) [mM:\'] (\d+) [sS\']*', tps, re.X)
    if matcher != None:
        return float(matcher.group(1))/60. + float(matcher.group(2))/3600.
    else:
        raise ValueError("Format invalide pour le temps {}".format(tps))

def heures_2_temps(h):
    """
        >>> for h in 1.54444, 0.2, 0.152, 0.08333:
        ...     print( h, heures_2_temps(h))
        1.54444 1°32'39''
        0.2 12'00''
        0.152 9'07''
        0.08333 4'59''
    """
    from math import fmod
    secs = h * 3600
    secsrest = fmod(secs, 60)
    mins = (secs - secsrest) / 60
    minsrest = fmod(mins, 60)
    h = (mins - minsrest) / 60

    fmth = "{h:d}°".format(h=int(h)) if h > 0 else ""
    return fmth + "{_m:d}'{_s:02d}''".format(_m=int(minsrest), _s=int(secsrest))

# ----------------------------------------------------------------

def requete(liste, filtre, format, detail=False):
    """ execute une recherche dans une liste
        renvoie la liste
    """

    maListe = [c for c in liste if filtre(c)]
    print( format.format(len(maListe)))
    if detail:
        for c in maListe:
            print( c)
    return maListe

# ----------------------------------------------------------------

def stats(listeperfs, label=None, geo=False, detail=False, pond=True, nb_max_perfs = 1000):
    """ analyse une liste de perfs
    """

    print( "\nstats de", label, len(listeperfs), 'perfs')
    total_brut = 0
    total_pondere = 0
    total_interlabos = 0
    total_theorique = 0
    tps_tot, dist_tot, deniv_tot, pts_tot = 0, 0, 0, 0
    fact = 1
    from collections import Counter
    tags = Counter()

    for i, p in enumerate(reversed(sorted(listeperfs, key=lambda a: a.points))):
        if i == nb_max_perfs:
            print( "arrêt des points à", nb_max_perfs, "courses")
            fact = 0

        j = i+1
        print( "   ", j, p)
        print( "       {:5.1f} pts".format(p.points),)

        total_brut += fact * p.points
        total_theorique += p.points
        pts_tot   += fact * p.points
        tps_tot   += p.heures
        dist_tot  += p.course.dist
        deniv_tot += p.course.deniv
        for t in p.course.tag.split():
            tags[t] += 1

        if pond:
            ponderation = pow(j, pow(0.95, (0.1 * j))) - pow(j - 1, pow(0.95, (0.1 * (j - 1))))
            ponderation = max(0.1, ponderation) # sinon la 50ème perf fait des points négatifs !
            print( " {:5.1f} corr. ({:-5.1%})".format(p.points*ponderation, ponderation-1))
            total_pondere += fact * p.points*ponderation
        else:
            total_pondere += fact * p.points
            ponderation = 1

        if p.course.tag == "interlabo":
            total_interlabos += fact * p.points*ponderation

        print()

    import re
    rePodium = re.compile(r'^([123])\b')
    pods = [0, 0, 0, 0]
    pods_cat = [0, 0, 0, 0]
    for p in listeperfs:
        matched = rePodium.match(p.scratch)
        if matched:
            place = int(matched.group(1))
            pods[place] += 1
            pods[0] += 1
        matched = rePodium.match(p.cat)
        if matched:
            place = int(matched.group(1))
            pods_cat[place] += 1
            pods_cat[0] += 1

    print()
    nb = len(listeperfs)
    #tps_tot = sum( [p.heures for p in listeperfs] )
    #dist_tot = sum( [p.course.dist for p in listeperfs] )
    #deniv_tot = sum( [p.course.deniv for p in listeperfs] )
    #pts_tot = sum( [p.points for p in listeperfs] )
    if nb != 0:
        print( "    total en {} perfs : {:.1f} km et {:.1f} m+ en {:.1f} h -> {:.1f} points".format(nb, dist_tot, deniv_tot, tps_tot, total_pondere),)
        print( "({:.1f} points perdus à cause de la limite, soit {:.1%})".format(total_theorique-total_brut, 1.-total_brut/total_theorique))
        print( "        soit en moyenne {:.1f} km et {:.1f} m+ en {:.1f} h = soit {:.2f} km/h -> {:.1f} points".format(dist_tot/nb, deniv_tot/nb, tps_tot/nb, dist_tot/tps_tot, total_pondere/nb))
        if pond:
            print( "        ({:.1f} points perdus par la pondération, soit {:.1%})".format(total_brut-total_pondere, total_brut/total_pondere-1.))
        print( "        ({:.1f} points gagnés sur les interlabo, soit {:.1%})".format(total_interlabos, total_interlabos/total_pondere))
        print( "    (%s)" % (", ".join( [ "%d x %s" % (tags[t], t) for t in sorted(tags.keys(), key= lambda a: tags[a]) ] )))
        if pods[0]:
            print( "    {} podiums".format(pods[0]),)
            print( " : {} x 1er, {} x 2ème, {} x 3ème".format(pods[1], pods[2], pods[3]))
        if pods_cat[0]:
            print( "    {} podiums par catégorie".format(pods_cat[0]),)
            print( " : {} x 1er, {} x 2ème, {} x 3ème".format(pods_cat[1], pods_cat[2], pods_cat[3]))


        if geo:
            geographie(listeperfs)

    return nb, tps_tot, dist_tot, deniv_tot, pts_tot, total_pondere, pods, pods_cat

# ----------------------------------------------------------------

def geographie(liste, label=None):
    """ analyse les départements d'une liste de perfs """

    print( "\ndépartements",)
    if label:
        print( "de", label)
    else:
        print()

# on compte les courses par départ
    from collections import Counter
    departs = Counter()
    for p in liste:
#        departs[p.course.depart] += p.course.difficulte()   # par difficulté
#        departs[p.course.depart] += p.course.dist           # par distance  (plantage à cause du 24h)
#        departs[p.course.depart] += 1                       # par nb de perfs
#        departs[p.course.depart] += 1./len(p.course.perfs)  # ?
        departs[p.course.depart] += p.heures  # ?
        # hack: infernal trail
        if p.course.nom == "Infernal Trail des Vosges":
            departs[p.course.depart] += 24.

# passage en log pour colorer aussi les petites valeurs
    from math import log10
    for depart in departs.keys():
        #print( depart, departs[depart])
        departs[depart] = log10(departs[depart])

# définition de la colormap
    cmax = max(departs.values())
    cmin = min(departs.values()) - 1   # j'enlève 1 (soit 10 km) car sinon la valeur min est traduite en blanc par la cmap
    plt.cm.register_cmap(name='coolwarm', data=mycolors._coolwarm_data)
    plt.cm.register_cmap(name='cea', data=mycolors._coolwarm_cea)
    cmap = plt.get_cmap('cea')#coolwarm')#OrRd')#Reds')
    def htmlRgb(mag):#, cmin, cmax):
        [r,g,b] = cmap(float(mag-cmin)/float(cmax-cmin))[0:3]
        return "#%02x%02x%02x" % (int(r*255), int(g*255), int(b*255))

# code pour le svg
    styles = ""
    for depart in reversed(sorted(departs.keys(), key=lambda a: departs[a])):
        value = departs[depart]
        styles += ".departement{depart} {{ fill: {color}; }} /* {value:7.1f} -> {log:.3f} */\n".format( depart=depart, color=htmlRgb(value), value=pow(10, value), log=value )

    with open('geo.cmap', 'w') as fgeo:
        fgeo.write(styles)

# colorscale
    x1, x2, xt = 4, 40, 50
    y1, y2, yt = 200, 220, 210
    colorscale = ""
    scale = np.logspace(cmax, cmin+1, 7, endpoint=True)

    for km in scale:
        scalekm = log10(km)
        arrondi = round(int(km), -1)
        if km > 1000: arrondi = round(int(km), -2)
        if km < 100: arrondi = int(km)
        colorscale += """
    <path
        style="fill-rule: evenodd; stroke: rgb(51, 51, 51); stroke-width: 1px; stroke-linecap: butt; stroke-linejoin: miter; stroke-opacity: 1;"
        d="M {x1:d},{y1:d} L {x2:d},{y1:d} L {x2:d},{y2:d} L {x1:d},{y2:d} L {x1:d},{y1:d}"
        id="pathcolor2"
        sodipodi:nodetypes="ccc"
        fill="{color}"/>
    <text
        xml:space="preserve"
        style="font-size:9x;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;stroke-opacity:1;fill:#000000;fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;font-family:Sans;-inkscape-font-specification:Sans"
        x="{xt:d}" y="{yt:d}"
        id="textcolor1">
        <tspan
        sodipodi:role="line"
        id="tspan2523"
        x="{xt:d}"
        y="{yt:d}"
        style="font-size:11px;font-style:normal;-inkscape-font-specification:Sans">{val:d} h</tspan></text>
    """.format(x1=x1, x2=x2, xt=xt, y1=y1, y2=y2, yt=yt,
               color=htmlRgb(scalekm), val=arrondi)
        #print( km, scalekm, htmlRgb(scalekm))
        y1 += 20
        y2 += 20
        yt += 20
        #print( km)

    fdeps = open("departs.svg", "r")
    with open("geographie.svg", "w") as fsvg:
        for line in fdeps:
            fsvg.write(line)
            import re
            if re.search(r'<!-- colorscale -->', line):
                fsvg.write(colorscale)
    fdeps.close()


def histo(perfs):
    import ROOT
    from ROOT import gROOT, TCanvas, TPad, gStyle, TH1F
    gROOT.Reset()
    gStyle.SetOptStat(False)
    c1 = TCanvas("c1", "Distances", 200, 10, 700, 700)
    #hdist = TH1F("dist", "km", 100, 0, 100)
    from array import array
    bins = array( 'f', [1, 5, 9, 15, 22, 30, 41, 50, 70, 101])#, 200, 500])
    hdist = TH1F("dist", "nb participants = f(difficulté)", len(bins)-1, bins)
    bins = array( 'f', [0, .25, .5, 1., 2., 4., 8., 15.])
    htmps = TH1F("heures", "h", len(bins)-1, bins)

    for p in perfs:
        hdist.Fill(p.course.diff)
        #htmps.Fill(p.heures)

    hdist.print(("all"))
    #c1.Divide(2, 1)
    c1.cd(1)
    return hdist #hdist.Draw()
    #c1.cd(2)
    #htmps.Draw()
