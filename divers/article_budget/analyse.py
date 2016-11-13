#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pandas as pd
pd.options.display.max_rows = 20
pd.options.display.max_columns = 5
pd.options.display.precision = 2    # 2 <=> 1 chiffre après la virgule

# ----------------------------------------------------------------
# chargement des données à analyser

from load_xlsxs import * # fonctions et alias sur les colonnes

kDonneesPlottees = kDist
kDonneesPlottees = kTime
kDonneesPlottees = kAsc     # pas joli (gros écarts entre les courses et le reste)
kDonneesPlottees = kDiff

# pour produire le fichier xlsx à analyser,
#   aller sur la page rapport de SportTracks,
#   et copier/coller le tableau dans un fichier Excel
#   ATTENTION : virer la dernière ligne 'Total'
#   (je n'ai pas trouvé d'export de l'appli)
xlsxfile = "xPerso\\entrainement.xlsx"
xlsxfile = "Dev\\CaP\\perso\\rapport2015.xlsx"
data = load_data("C:\\Users\\fj221066\\Documents\\" + xlsxfile,
          wanted_sheet='saison')

# mise à l'équerre des données (formats...)
data = manip_xlsx_data(data)

# ----------------------------------------------------------------
# construction des données temporelles analysées (cumul hebdo)

grouper = pd.TimeGrouper(freq="1W", how='sum')
agg = data.groupby(grouper).agg({kDist: sum, kAsc: sum, kTime: sum, kDiff: sum})
print("\nagg :", type(agg))
print(agg)#.head())

# ----------------------------------------------------------------
# plot des données hebdo

import matplotlib.pyplot as plt
fig = plt.figure()
ax = plt.gca()
fig.autofmt_xdate()

import matplotlib.patches as patches
from bars import make_bar_path
import datetime

x = agg[kDonneesPlottees].index.values     # np.datetime64[ns]
x = [float(t)/1e9 for t in x]   # passage en timestamp (nb sec depuis epoch)
x = [t - 7*86400 for t in x]    # on enlève 7 jours car les barres ont pour origine le dernier jour de la semaine
y = agg[kDonneesPlottees].values
barpath = make_bar_path(x, y[:-1])
patch = patches.PathPatch(barpath)#, facecolor='green', edgecolor='yellow', alpha=0.5)
ax.add_patch(patch)

import matplotlib.ticker as ticker
def format_date(x, dummy):
    return datetime.date.fromtimestamp(x).strftime('%d/%m')
ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))

#import matplotlib.dates as mdates
#months = mdates.MonthLocator()  # every month
#ax.xaxis.set_major_locator(months) # marche pas

ax.set_xlim(x[0], x[-1])
ax.set_ylim(0, y.max()*1.1)
ax.set_ylabel(kDonneesPlottees)

# ----------------------------------------------------------------
# plot

courses = load_data("C:\\Users\\fj221066\\Documents\\" + xlsxfile,
          wanted_sheet='courses15', parse_cols="A:D;G")

# mise à l'équerre des données (formats...)
courses = manip_xlsx_data(courses)
# fusion activités de même nom (WEC, ITV...)
courses = merge_on_name(courses)

# TODO : harmoniser les colonnes avec celles des données SportTracks
ax.scatter([float(t)/1e9 for t in courses.index.values],
            courses[kDonneesPlottees],
            s=50,
            c='r', # or sequence
            marker='o',
            cmap=None, # if c is an array of float
            zorder=10  # sinon les ronds sont cachés par les barres
            )

j = 86400 # sec par jour
for i, c in courses.iterrows(): # ça renvoie un tuple
#    print('i= %s\nc= %s' % (i, c))
    plt.text(float(i.timestamp())+4*j,
             c[kDonneesPlottees]+(y.max()-y.min())/30.,
             c[kNom],
#             backgroundcolor='w',
             bbox=dict(boxstyle='round', facecolor='w', alpha=0.5)
             )


plt.savefig('annee.png')
plt.show()
