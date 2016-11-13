#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pandas as pd
import numpy as np
pd.options.display.max_rows = 20
pd.options.display.max_columns = 5
pd.options.display.precision = 2    # 2 <=> 1 chiffre après la virgule

# ----------------------------------------------------------------
# chargement des données à analyser

from load_xlsxs import * # fonctions et alias sur les colonnes

kDonneesPlottees = kAsc     # pas joli (gros écarts entre les courses et le reste)
kDonneesPlottees = kTime
kDonneesPlottees = kDist
kDonneesPlottees = kDiff

# pour produire le fichier xlsx à analyser,
#   aller sur la page rapport de SportTracks,
#   et copier/coller le tableau dans un fichier Excel
#   ATTENTION : virer la dernière ligne 'Total'
#   (je n'ai pas trouvé d'export de l'appli)
xlsxfile = "xPerso\\entrainement.xlsx"
xlsxfile = "Dev\\CaP\\perso\\planning\\rapport2015.xlsx"
wanted_sheet = 'saison'
xlsxfile = "Dev\\CaP\\perso\\planning\\planning.xlsx"
wanted_sheet = 'planning'
data = load_data("C:\\Users\\fj221066\\Documents\\" + xlsxfile,
          wanted_sheet=wanted_sheet)

# mise à l'équerre des données (formats...)
data = manip_xlsx_data(data)

# ----------------------------------------------------------------
# construction des données temporelles analysées (cumul hebdo)

grouper = pd.TimeGrouper(freq="1W", how='sum')
agg = data.groupby(grouper).agg({kDist: sum, kAsc: sum, kTime: sum, kDiff: sum})
print("\nagg :", type(agg))
print(agg)#.head())

# ----------------------------------------------------------------

today = datetime.datetime.now().timestamp()

# ----------------------------------------------------------------
# plot des données hebdo

import matplotlib.pyplot as plt

fig, axes = plt.subplots(nrows=2, ncols=2)
_axes = axes.flatten()
for ik, kDonneesPlottees in enumerate([kAsc, kTime, kDist, kDiff]):

    # fig = plt.figure()
    # ax = plt.gca()
    ax = _axes[ik]
    fig.autofmt_xdate()

    import matplotlib.patches as patches
    from bars import make_bar_path
    import datetime

    x = list(agg[kDonneesPlottees].index.values)     # np.ndarray de np.datetime64[ns], je passe par une liste pour rajouter un élément
    # print(x[0], type(x[0]))
    x.append(x[-1] + np.timedelta64(7, 'D'))    # dernière borne pour l'histo
    # print(x)
    x = [float(t)/1e9 for t in x]   # passage en timestamp (nb sec depuis epoch)
    x = [t - 7*86400 for t in x]    # on enlève 7 jours car les barres ont pour origine le dernier jour de la semaine
    y = agg[kDonneesPlottees].values
    barpath = make_bar_path(x, y)
    patch = patches.PathPatch(barpath)
    # ax.add_patch(patch)
    polys = patch.get_path().to_polygons()
    for date, p in zip(x, polys):
        color = 'b'
        if -7*86400 <= date - today < 0: # semaine en cours en rouge
            color = 'r'
        ax.add_patch(patches.Polygon(p, color=color, ec='k'))

    import matplotlib.ticker as ticker
    def format_date(x, dummy):
        return datetime.date.fromtimestamp(x).strftime('%d/%m')
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    
    ax.xaxis.set_ticks(x[::2])
    ax.xaxis.set_tick_params(direction='out')

    #import matplotlib.dates as mdates
    #months = mdates.MonthLocator()  # every month
    #ax.xaxis.set_major_locator(months) # marche pas

    ax.set_xlim(x[0], x[-1])
    ax.set_ylim(0, y.max()*1.1)
    ax.set_ylabel(kDonneesPlottees)

# ----------------------------------------------------------------
# plot

# courses = load_data("C:\\Users\\fj221066\\Documents\\" + xlsxfile,
          # wanted_sheet='courses15', parse_cols="A:D;G")

# # mise à l'équerre des données (formats...)
# courses = manip_xlsx_data(courses)
# # fusion activités de même nom (WEC, ITV...)
# courses = merge_on_name(courses)

# # TODO : harmoniser les colonnes avec celles des données SportTracks
# ax.scatter([float(t)/1e9 for t in courses.index.values],
            # courses[kDonneesPlottees],
            # s=50,
            # c='r', # or sequence
            # marker='o',
            # cmap=None, # if c is an array of float
            # zorder=10  # sinon les ronds sont cachés par les barres
            # )

# j = 86400 # sec par jour
# for i, c in courses.iterrows(): # ça renvoie un tuple
# #    print('i= %s\nc= %s' % (i, c))
    # plt.text(float(i.timestamp())+4*j,
             # c[kDonneesPlottees]+(y.max()-y.min())/30.,
             # c[kNom],
# #             backgroundcolor='w',
             # bbox=dict(boxstyle='round', facecolor='w', alpha=0.5)
             # )


plt.savefig('annee.png')
plt.show()
