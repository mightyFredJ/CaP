# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 12:13:17 2015

@author: FJ221066
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 21:01:19 2015

@author: FJ221066
"""

# cd c:/Users/fj221066/Documents/Dev/CaP/perso/
import pandas as pd
import matplotlib.pyplot as plt
import re
import sys

# A        B     C     D     E    F           G
# class	doss	nom	club	cat	classcat	temps	ecart	pays

motif_resu = r'^(:\s*)? (?P<class>\d+) \s .* (?P<temps>\d\d:\d\d:\d\d)'
reg_resu = re.compile(motif_resu, re.I | re.X)
reg_ascea = re.compile(r'(ASCEA|MBDA)', re.I | re.X)
reg_course = re.compile('_(\d+).*_(\S+km)\.', re.I | re.X)

xls_filename = './MontagnHard.xlsx'
xlResu = pd.ExcelFile(xls_filename)

kTps = 'Temps de course'
kTd  = 'pd.Timedelta'
kH   = 'h'

#plt.subplot(311)
for wanted_sheet in range(3):
    data = xlResu.parse(wanted_sheet,
#                        converters={kTps: lambda x: str(x)},
                        parse_cols="A,G",
#                        date_parser=lambda x: str(x),
#                        parse_dates=True, # sert à rien
#                        index_col='Ordre',
                        )
    sheet_name = xlResu.sheet_names[wanted_sheet]
    dist = sheet_name.replace('2015-', '') + ' km'
    print(dist, data.head())
    import datetime as dt
    def fun_conv(t):
        if t.__class__ == dt.time:
            return pd.Timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
        elif t.__class__ == dt.datetime:
            return pd.Timedelta(hours=t.hour + t.day*24, minutes=t.minute, seconds=t.second)
    data[kTd] = data[kTps].apply(fun_conv)
    data[kH] = data[kTd] / pd.Timedelta(hours=1)
#    print(data[::10])#.head())
    data['pc'] = data.index / len(data) * 100

    print(data[kH].describe())

    plt.plot(data['pc'], data[kH], label=dist)
    plt.xlabel('% des arrivants')
    plt.ylabel('durée (h)')
    plt.grid()
    plt.legend(loc='upper left')
    from matplotlib.lines import Line2D
    yy = 14.5
    plt.gca().add_line(Line2D([65, 65, 0], [0, yy, yy], color='k', ls='--'))

import matplotlib.ticker
plt.gca().yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(1))
plt.gca().yaxis.set_tick_params(which='minor', length=6)
plt.show()
