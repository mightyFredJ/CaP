# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 17:40:25 2015

@author: FJ221066
"""

import pandas as pd
pd.options.display.max_rows = 7
pd.options.display.max_columns = 120

import matplotlib.pyplot as plt
import numpy as np
np.set_printoptions(precision=3)

#%% ----------------------------------------------------------------
# config

config = {
    'annee': '2015-2016',
    'sheet': 0,
    'refdate': '2015-10-01',
}
# config = {
    # 'annee': '2016-2017',
    # 'sheet': 1,
    # 'refdate': '2016-10-01',
# }

#%% ----------------------------------------------------------------
# chargement

xls_filename = '../../../xPerso/ASCEA/Section_CàP_2016-2017.xlsx'
wanted_sheet = config['sheet']
xlAdherents = pd.ExcelFile(xls_filename)
data = xlAdherents.parse(wanted_sheet, skiprows=3, parse_cols="A:E", index_col=[0, 1], skip_footer=8)#index_col=['Nom', 'Prénom'])#, parse_dates=['Date'])#sheet_name=9)#wanted_sheet)#, skiprows=range(17))
print(data)
print()

# calcul age à partir date naissance
data['age'] = pd.to_datetime(config['refdate']) - data['Date naiss.']
data['age'] = [ int(j.days/365) for j in data['age'] ]
print(data)
print('moy. = %d ans' % data['age'].mean())
print()

pd.options.display.max_rows = 0
print(data.sort_values('age'))#.tail(30))

#%% ----------------------------------------------------------------
#%% prépa zone dessin

# x = ages.size().index
# y = ages.size().values
amin, amax = min(data['age']), max(data['age'])
# binmin, binmax = amin//5*5, ((amax//5)+1)*5

fig = plt.figure()

#%% ----------------------------------------------------------------

sexes = data.groupby('Sexe')
prev_top = None
colors = {'F': 'm', 'M': 'b'}
for sex, dfsex in sexes:
    # print(sex)
    # print(dfsex.head())
    # print()

    # ages = dfsex.groupby('age')

    hist, bins = np.histogram(dfsex['age'], bins=range(20, 75, 5)) #(binmax-binmin)/5 )
    # print(hist, bins, sep='\n')
    width = (bins[1] - bins[0]) * 0.8
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width, bottom=prev_top, facecolor=colors[sex])
    prev_top = hist

ymax = 23
plt.gca().set_ylim(0, ymax)
yarrow = 22
argsarrows = {'color': 'k', 'lw': 2}

limits = [20, 40, 50, 60, 70]
cats = "S V1 V2 V3".split()
for ilim, limit in enumerate(limits):
    if ilim > 0 and ilim < len(limits)-1:
        plt.axvline(limit, 0, yarrow/ymax, ls='dashed', **argsarrows)
    if ilim > 0:
        x = limits[ilim-1]
        dx = limit-limits[ilim-1]
        # plt.arrow(x, yarrow, dx, 0, width=0.02, length_includes_head=True, **argsarrows)
        # plt.arrow(limit, yarrow, -dx, 0, width=0.02, length_includes_head=True, **argsarrows)
        plt.text(x+dx/2., yarrow-1, cats[ilim-1], ha='center')
    
moyenne = data['age'].mean()
print("moyenne = %.2f ans" % moyenne)
mois = (moyenne - int(moyenne)) * 12
plt.text(30, 15, r'$\bar{x} = %d\ ans\ %d\ mois$' % (moyenne, mois), ha='center', size='x-large')

plt.xlabel('âge')
plt.ylabel('nb. d\'adhérents')

plt.show()
imgname = 'ages_section_%s.png' % config['annee']
print('sauvegarde sous', imgname)
fig.savefig(imgname)
