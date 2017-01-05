# -*- coding: utf-8 -*-
"""
"""

# ---- python ----
from datetime import datetime, timedelta

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

# ---- objectif ----

objectif = {
    'name': 'MH100',
    'date': datetime(2017, 7, 8),
    'dist': 108,
    'D+':   8100,
}
objectif = {
    'name': 'MV',
    'date': datetime(2017, 3, 5),
    'dist': 47,
    'D+':   1700,
    'fpre': 0.8,    # fact à appliqué à la pré-prépa
}

# ---- prépa ----

prepa = {
    # 2 macro-cycles, progression constante
    'name': "progress",
    'data': [55, 66, 77, 39,  # base 100
             77, 88, 99, 50,
             23],
    'pre':  [33, 44, 28, 33],
}
#prepa = {
#    # mode WEC
#    'name': "WECs",
#    'data': [80,  20, 100,
#             20,  60, 100,
#             20,  40,  20],
#    'pre':  [50, 65, 60, 35, 50, 25],
#}


#%% manip des données --------------------------------------------------------

# objectif
x_obj, y_obj = -1+.4, objectif['dist'] + objectif['D+']/100.

# prépa
n = len(prepa['data'])  # nb semaines prépa
x = np.arange(-n, 0)  # indices cols prépa
y = np.ones(n) * prepa['data'] / 100. * y_obj

# avant la prépa
n_pre = len(prepa['pre'])
x_pre = np.arange(-n-n_pre, -n)
y_pre = prepa['pre']
if 'fpre' in objectif:
    y_pre = [yy * objectif['fpre'] for yy in y_pre]
pre_ymin, pre_ymax = min(y_pre), max(y_pre)

# dates
mondays = [objectif['date'] + ((i+1) * 7 - 6) * day for i in x]
mondays_labels = [m.strftime('%d/%m') for m in mondays]
weeks_labels = ["S %d" % i for i in x]
#mondays_labels = ["S -%d\n%s" % (i, m) for i, m in enumerate(mondays_labels)]
#print("lundis :", pformat(list(zip(x, mondays_labels))))


#%% plot ---------------------------------------------------------------------

fig = plt.figure()

# ---- qqs constantes
ymax = y_obj + 20
pre_color = '0.5'
prepa_color = 'b'
obj_color = 'r'
show_y_scale = True

# ----  barres
plt.bar(x_pre -.4, y_pre, ls='dashed', color=pre_color)
plt.bar(x - .4, y, color=prepa_color)

# ---- objectif
plt.gca().add_patch(Ellipse((x_obj, y_obj), .5, 5*(y_obj/100.),
                            facecolor=obj_color, zorder=20))
plt.gca().add_line(Line2D((x_obj, x_obj), (y[-1], y_obj),
                   linestyle='dashed', color=obj_color, zorder=0))
plt.annotate(s=objectif['name'], xy=(x_obj, y_obj+2.4), xytext=(-1, y_obj+10),
             arrowprops=dict(arrowstyle="->"), backgroundcolor='w',
             color=obj_color,
             horizontalalignment='left')

# ---- axes, labels & ticks

plt.xlabel('Semaine $\longrightarrow$')
plt.ylabel('Charge $\longrightarrow$')
if not show_y_scale:
    plt.yticks([])
plt.ylim(ymax=ymax)

# 2 échelles perso pour x : dates et n° de semaines
upper_labels = weeks_labels
lower_labels = mondays_labels

# échelle du bas :
tickstep = 2
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
    plt.annotate(s='ultra', xy=(x[9-9], y[9-9]),# xytext=(-1, y_obj+10),
                 arrowprops=dict(arrowstyle="->"), color=prepa_color)
    plt.annotate(s='WEC', xy=(x[9-7], y[9-7]),# xytext=(-1, y_obj+10),
                 arrowprops=dict(arrowstyle="->"), color=prepa_color)
    plt.annotate(s='WEC', xy=(x[9-4], y[9-4]),# xytext=(-1, y_obj+10),
                 arrowprops=dict(arrowstyle="->"),  color=prepa_color)

# ---- ça suffit pour aujourd'hui

plt.savefig('plan-%s-%s.png' % (objectif['name'], prepa['name']))

plt.show()

