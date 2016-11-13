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
reg_course = re.compile('_(\d+).*_([^_]+)\.txt', re.I | re.X)

for fichier in [
        "trailblanc_2016_nocturne_6km.txt",
        "trailblanc_2016_18km.txt",
#        "trailblanc_2016_challenge.txt",
#        "trailblanc_2015_nocturne_6km.txt",
#        "trailblanc_2014_nocturne_5,5km.txt",
#        "trailblanc_2014_17km.txt",
#        "trailblanc_2013_18km.txt"
        ]:
    raw_data = { 'class': [], 'temps': [] }
    cea_data = { 'class': [], 'temps': [] }

    annee, dist = reg_course.search(fichier).group(1, 2)

    with open(fichier, "br") as ftxt:
        for line in ftxt:
            try:
                sline = line.decode(encoding="utf-8",)
                matcher_resu = reg_resu.match(sline)
                if matcher_resu:
                    raw_data['class'].append(matcher_resu.group('class'))
                    raw_data['temps'].append(matcher_resu.group('temps'))
                matcher_cea = reg_ascea.search(sline)
                if matcher_cea:
                    cea_data['class'].append(matcher_resu.group('class'))
                    cea_data['temps'].append(matcher_resu.group('temps'))
            except UnicodeDecodeError as ex:
                print(ex, line)
    #        raise(BaseException(str(ex) + line))

    data = pd.DataFrame(raw_data)
    #    data = xl.parse(sheetname=page,
#                    converters={'temps': lambda x: str(x)},
##                    index_col=0,
#                    parse_cols="A,E:G")
    data['h'] = pd.to_timedelta(data['temps']) / pd.Timedelta(hours=1)
    data['pc'] = data.index / len(data)
    print(data.head())
    print(data['h'].describe())

#    plt.plot(data['pc'], data['h'])
#    data['h'].hist(bins=20)
    n, bins, patches = plt.hist(data['h'],
                                bins=10, normed=False, histtype='step',
                                label='{dist}'.format(**locals()))
    print('n=', n)
    print('bins=', bins)
    print('patches=', patches)
    def get_y_for_x(x):
        for i in range(len(n)-1):
            if bins[i] < x and x < bins[i+1]:
                return n[i]
        return 0

    print('%d CEA' % len(cea_data['class']))
    if len(cea_data['class']) > 0:
        data = pd.DataFrame(cea_data)
        data['h'] = pd.to_timedelta(data['temps']) / pd.Timedelta(hours=1)
        data['pc'] = data.index / len(data)
        data['y'] = data['h'] # ?
        for i in range(len(data['h'])):
            data.loc[i,'y'] = get_y_for_x(data['h'][i])
        print(data.head())
        plt.scatter(data['h'], data['y'], c='r', marker='o', s=40, label='CEA')

#
from matplotlib.ticker import FuncFormatter
from datetime import time
# x en h mais je veux des hh:mm sur l'axe
def myfmt(x, dummy):
    h = int(x)
    m = int((x - h) * 60)
    return time(hour=h, minute=m).strftime('%H:%M')
plt.gca().xaxis.set_major_formatter(FuncFormatter(myfmt))
plt.ylim(ymin=0)
plt.legend()
plt.xlabel('Temps')
plt.ylabel('Arrivants')
plt.show()
##data['h'].hist(bins=20)
