# -*- coding: utf-8 -*-
"""
"""

# ---- python ----
from datetime import datetime, timedelta
import calendar

# ---- other ----
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.lines import Line2D

# ---- mine ----


#%% qqs trucs génériques -----------------------------------------------------

# pandas
pd.options.display.max_rows = 7
pd.options.display.precision = 1 # ou pd.set_option('precision',1)

# numpy
np.set_printoptions(precision=3)

# matplotlib
plt.xkcd()

# manip dates
day = timedelta(days=1)

#%% données brutes -----------------------------------------------------------

# ---- Vulcain ----

objectif = {
    'name': 'MV47',
    'date': datetime(2017, 3, 5),
    'dist': 47,
    'D+':   1700,
    'fpre': 0.8,    # fact à appliqué à la pré-prépa
}
#objectif = {
#    'name': 'UV73',
#    'date': datetime(2017, 3, 5),
#    'dist': 73,
#    'D+':   2500,
#    'fpre': 1.0,    # fact à appliqué à la pré-prépa
#}

ref_prepa = {
    # 2 macro-cycles, progression constante
    'name': "progress",
    'data': [55, 66, 77, 39,  # base 100
             77, 88, 99, 50,
             23],
    'pre':  [33, 44, 28, 33],
}

prepa = {
    # 2 macro-cycles, progression constante
    'name': "progress",
    'data': [55, 66, 77, 39,  # base 100
             77, 88, 99, 50,
             23],
    'pre':  [33, 44, 28, 33],
}

#ref_prepa = {
#    'data': [80,  20, 100,
#             20,  60, 100,
#             20,  40,  20],
#    'labels': ['ultra', '', '',
#               'WEC', '', 'WEC',
#               '', '', ''],
#}
#
#prepa = {
#    'name': "WECs",
#    'data': [80,  20, 100,
#             20,  60, 100,
#             20,  40,  20],
#    'pre':  [50, 65, 60, 35, 50, 25],
#}

intermediaires = [
    {
        'name': 'Raid28',
        'date': '22/1',
        'dist': 55,
        'D+':   1000,
    },
]

#
## ---- MontagnHard ----
#
#objectif = {
#    'name': 'MH100',
#    'date': datetime(2017, 7, 8),
#    'dist': 108,
#    'D+':   8100,
#}
#
#ref_prepa = {
#    'data': [80,  20, 100,
#             20,  60, 100,
#             20,  40,  20],
#    'labels': ['ultra', '', '',
#               'WEC', '', 'WEC',
#               '', '', ''],
#}
#
#prepa = {
#    # mode WEC
#    'name': "WECs",
#    'data': [80,  20,  60,
#            100,  40, 100,
#             20,  40,  20],
#    'pre':  [50, 65, 60, 35, 50, 25],
#}
#
#intermediaires = [
#    {
#        'name': 'UTC',
#        'date': datetime(2017, 5, 13),
#        'dist': 104,
#        'D+':   4000,
#    },
#    {
#        'name': 'Gypaëte',
#        'date': datetime(2017, 6, 3),
#        'dist': 70,
#        'D+':   4000,
#    },
#    {
#        'name': 'Samoëns',
#        'date': datetime(2017, 6, 17),
#        'dist': 86,
#        'D+':   6000,
#    },
#]
#
#
## ---- UT4M ----
#
#objectif = {
#    'name': 'UT4M',
#    'date': datetime(2017, 8, 17),
#    'dist': 169,
#    'D+':   11000,  # diff 280
#    'prepamax': 180,
#}
#objectif = {
#    'name': 'Montreux',
#    'date': datetime(2017, 7, 28),
#    'dist': 165,
#    'D+':   13600,  # diff 300
#    'prepamax': 180,
#}
#objectif = {
#    'name': 'Suisse',
#    'date': datetime(2017, 9, 1),
#    'dist': 165,
#    'D+':   11800,  # diff 280
#    'prepamax': 180,
#}
#objectif = {
#    'name': 'ITV',
#    'date': datetime(2017, 9, 8),
#    'dist': 200,
#    'D+':   10400,  # diff 300
#    'prepamax': 180,
#}
#
#ref_prepa = {
#    'data': [50,  65,  80,  30,
#             60,  70,  40,
#             80,  20,  80,  20,
#             80,  20, 100,
#             20,  60, 100,
#             20,  40,  20],
#    'labels': ['', '', 'volume', '',
#               '', 'trail', '',
#               'WEC', '', '', '',
#               'ultra', '', 'WEC',
#               '', '', 'WEC',
#               '', '', ''],
#}
#
#prepa = {
#    # mode WEC
#    'name': "WECs",
#    'data': [50,  65,  80,  30,
#             60,  70,  40,
#             70,  20,  40,  20,
#             80,  20, 100,
#             20,  60, 100,
#             20,  40,  20],
#    'pre':  [50, 65, 60, 35, 50, 25],
#}
#
#intermediaires = [
#    { 'name': 'UTC', 'date': '13/5', 'dist': 104, 'D+': 4000, },
#    { 'name': 'Gypaëte', 'date': '3/6', 'dist': 70, 'D+': 4000, },
#    { 'name': 'Samoëns', 'date': '17/6', 'dist': 86,  'D+': 6000,  },
#    { 'name': 'AMT', 'date': '24/6', 'dist': 93, 'D+': 4800, },
#    { 'name': 'MH100', 'date': '8/7', 'dist': 108, 'D+': 8100, },
#    { 'name': 'UTB', 'date': '22/7', 'dist': 100, 'D+': 6000, },
#    { 'name': 'TdFiz', 'date': '30/7', 'dist': 60, 'D+': 5000, },
#    { 'name': 'Ut4M', 'date': '18/8', 'dist': 100, 'D+': 5500, },
#]


#%% manip des données --------------------------------------------------------

# mise en forme python des données user-friendly

def ekm(km, deniv):
    return km + deniv/100.

for inter in intermediaires:
    inter['date'] = datetime.strptime(inter['date'] + '/17', '%d/%m/%y')
    inter['diff'] = ekm(inter['dist'], inter['D+'])


# objectif
x_obj, y_obj = -1, ekm(objectif['dist'], objectif['D+'])
if not 'prepamax' in objectif:
    objectif['prepamax'] = y_obj

# prépa
n = len(prepa['data'])  # nb semaines prépa
x = np.arange(-n, 0)  # indices cols prépa
y = np.ones(n) * prepa['data'] / 100. * objectif['prepamax']
y_ref = np.ones(n) * ref_prepa['data'] / 100. * objectif['prepamax']

# avant la prépa
n_pre = len(prepa['pre'])
x_pre = np.arange(-n-n_pre, -n)
y_pre = prepa['pre']
if 'fpre' in objectif:
    y_pre = [yy * objectif['fpre'] for yy in y_pre]
pre_ymin, pre_ymax = min(y_pre), max(y_pre)

# dates
run_day = calendar.weekday(objectif['date'].year, objectif['date'].month, objectif['date'].day)
print('course le', objectif['date'].year, objectif['date'].month, objectif['date'].day)
print('c\'est un', run_day, '(' + calendar.day_name[run_day] + ')')

mondays = [objectif['date'] + ((i+1) * 7 - run_day) * day for i in x]
mondays_labels = [m.strftime('%d/%m') for m in mondays]
weeks_labels = ["S %d" % i for i in x]
print("1er lundi de la prépa : %s (S %d)" % (mondays_labels[0], x[0]))


#%% plot ---------------------------------------------------------------------

figsize = (8,6)  # défaut : matplotlib.rcParams['figure.figsize'] = (8,6)
if n + n_pre > 15:
    figsize=(12,6)

fig = plt.figure(figsize=figsize)

# ---- qqs constantes
ymax = y_obj + 20

show_y_scale = True
bw = 0.4  # barwidth
shift = 0.1


pre_color = '0.6'
prepa_color = 'b'
obj_color = 'r'
int_color = 'g'
ref_color = '0.3'

# ----  barres
plt.bar(x_pre - bw/2.  , y_pre, color=pre_color, width=bw, ls='dashed')
plt.bar(x - bw/2. - shift, y,     color=prepa_color, width=bw)
plt.bar(x - bw/2. + shift, y_ref+1, color=ref_color, width=bw, zorder=0)  # zorder : derrière

# ---- objectif
plt.gca().add_patch(Ellipse((x_obj, y_obj), .5, 5*(ymax/100.),
                            facecolor=obj_color, zorder=20))
plt.gca().add_line(Line2D((x_obj, x_obj), (y[-1], y_obj),
                   linestyle='dashed', color=obj_color, zorder=0))
plt.annotate(s=objectif['name'], xy=(x_obj, y_obj+2.4), xytext=(-1, y_obj+10),
             arrowprops=dict(arrowstyle="->"), backgroundcolor='w',
             color=obj_color,
             horizontalalignment='left')


# ---- intermédiaires
for inter in intermediaires:
    for i, monday in enumerate(mondays[:-1]):
        if monday <= inter['date'] < mondays[i+1]:
            x_int, y_int = i - n, ekm(inter['dist'], inter['D+'])
            plt.gca().add_patch(Ellipse((x_int, y_int), .2, 2*(ymax/100.),
                                facecolor=int_color, zorder=20))
            plt.annotate(s=inter['name'], xy=(x_int, y_int),
                         xytext=(x_int+.2, y_int+10),
                         arrowprops=dict(arrowstyle="->"), #backgroundcolor='w',
                         color=int_color,
                         horizontalalignment='left')
            break

# ---- axes, labels & ticks

plt.xlabel('Semaine $\longrightarrow$')
plt.ylabel('Charge $\longrightarrow$')
if not show_y_scale:
    plt.yticks([])
plt.xlim(xmin=-n-n_pre-1)
plt.ylim(ymax=ymax)

# 2 échelles perso pour x : dates et n° de semaines
upper_labels = weeks_labels
lower_labels = mondays_labels

# échelle du bas :
tickstep = 2
#if n + n_pre > 15:
#    tickstep = 3
plt.xticks(x[::tickstep], lower_labels[::tickstep])

# faire croire qu'on a une 2ème échelle en haut :
#   recette extraite de matplotlib.boxplot_demo2.py :
ax1 = plt.gca()
for tickpos, label in zip(ax1.get_xticks(), upper_labels[::tickstep]):
    ax1.text(tickpos, ymax + 2, label, ha='center')

# ---- annotations

# phase avant la préparation
xp1, xp2 = x_pre[0] - .5, x_pre[-1] + .5
yp1, yp2 = pre_ymax, pre_ymax + 5
poly = Line2D([xp1, xp1, xp2, xp2], [yp1, yp2, yp2, yp1], color=pre_color)
plt.gca().add_line(poly)
plt.text((xp1+xp2)/2., yp2 + 5, "niveau actuel", color=pre_color, ha='center')

if prepa['name'] == "progress":
    # mésocycles
    for i in range(int(n/4)):
        x1, x2 = x[i*4+0] - .5, x[i*4+3] + .5
        y1 = max(y[i*4:i*4+4])
        y2 = y1 + 5
        poly = Line2D([x1, x1, x2, x2], [y1, y2, y2, y1], color=prepa_color)
        plt.gca().add_line(poly)
        plt.text((x1+x2)/2., y2 + 5, "Méso-cycle %d" % (i+1),
                 color=prepa_color, ha='center')

elif prepa['name'] == "WECs":
    for i, lbl in enumerate(ref_prepa['labels']):
        if lbl is '':
            continue
        plt.annotate(s=lbl, xy=(x[i]+.1, y_ref[i]), xytext=(x[i]+.2, y_ref[i]+10),
                     arrowprops=dict(arrowstyle="->"), color=ref_color)

# ---- ça suffit pour aujourd'hui

plt.savefig('plan-%s-%s.png' % (objectif['name'], prepa['name']))

plt.show()

