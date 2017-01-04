# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 17:40:25 2015

@author: FJ221066
"""

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.lines import Line2D

from datetime import datetime, timedelta
from pprint import pformat

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

runday = datetime(2017, 3, 5)

# 2 macro-cycles, progression constante
name = "progress"
data = [50, 60, 70, 35,
        70, 80, 90, 45,
        20]
n_pre = 4
y_pre = [30, 40, 25, 30]
pre_min, pre_max = 25, 45

# mode WEC
#name = "WEC"
#data = [ 90,  20, 110,
#         20,  60, 110,
#         20,  40,  20]
#n_pre = 6
#pre_min, pre_max = 45, 75


#%% manip des données --------------------------------------------------------

n = len(data)  # nb cols prépa
x = np.arange(-n, 0)  # indices cols prépa
x_pre = np.arange(-n-n_pre, -n)
#y_pre = np.random.randint(pre_min, pre_max, size=n_pre)

mondays = [runday + ((i+1) * 7 - 6) * day for i in x]
mondays_labels = [m.strftime('%d/%m') for m in mondays]
mondays_labels = ["S %d" % i for i in x]
#print("lundis :", pformat(list(zip(x, mondays_labels))))


#%% plot ---------------------------------------------------------------------

fig = plt.figure()

# avant-prépa
#print(x_pre, y_pre)
plt.bar(x_pre -.4, y_pre, ls='dashed', color='0.5')
# prépa
plt.bar(x - .4, data)

# objectif
x_obj, y_obj = -1+.4, max(data)
plt.gca().add_patch(Ellipse((x_obj, y_obj), .5, 5, facecolor='r'))
plt.gca().add_line(Line2D((x_obj, x_obj), (data[-1], y_obj),
                   linestyle='dashed', color='k', zorder=0))
plt.annotate(s='objectif', xy=(x_obj+.24, y_obj+2.4), xytext=(-1, y_obj+10),
             arrowprops=dict(arrowstyle="->"), backgroundcolor='w',
             horizontalalignment='left')

plt.xlabel('Semaine $\longrightarrow$')
plt.xticks(x[::2], mondays_labels[::2])
plt.ylabel('Charge (heures ou km/mD+) $\longrightarrow$')
plt.yticks([])
plt.ylim(ymax=max(data)+20)

xp1, xp2 = x_pre[0] - .5, x_pre[-1] + .5
yp1, yp2 = pre_max, pre_max + 5
poly = Line2D([xp1, xp1, xp2, xp2], [yp1, yp2, yp2, yp1], color='0.5')
plt.gca().add_line(poly)
plt.text((xp1+xp2)/2., yp2 + 5, "niveau actuel", color="0.5", ha='center')

if name == "progress":
    for i in range(int(n/4)):
        x1, x2 = x[i*4+0] - .5, x[i*4+3] + .5
        y1 = max(data[i*4:i*4+4])
        y2 = y1 + 5
        poly = Line2D([x1, x1, x2, x2], [y1, y2, y2, y1], color='b')
        plt.gca().add_line(poly)
        plt.text((x1+x2)/2., y2 + 5, "Méso-cycle %d" % (i+1), color="b", ha='center')


plt.savefig('plan-%s.png' % name)

plt.show()

