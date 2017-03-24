# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 22:46:10 2015

@author: FJ221066
"""


import pandas as pd
pd.options.display.max_rows = 20
pd.options.display.max_columns = 5
import matplotlib.pyplot as plt

from datetime import datetime, timedelta

annee = pd.date_range('01-01-2015', periods=12, freq='M')
print(annee)

kms = [float(i) for i in """244
248
373
311
388
261
319
370
329
216
305
226
""".split()]
print(kms)

df = pd.DataFrame({'kms': kms}, index=annee)
print(df.head())

def format_date(x, dummy):
    dt = df.index[x]
    fmt = dt.strftime('%b')
    return fmt

import matplotlib.ticker as ticker
df['kms'].plot(kind='bar')
plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
plt.gcf().autofmt_xdate()

import io
courses = pd.read_csv(io.StringIO("""date;km;course
01/04/2015;42;Marathon Cernay
01/18/2015;50;Semi Raid 28
03/21/2015;78;EcoTrail
04/11/2015;112;UBVT
06/20/2015;90;TVL
08/13/2015;100;WEC
09/12/2015;164;ITV
12/05/2015;72;SaintéLyon
"""), sep=";", parse_dates=[0])

print(courses.head())
print(courses.iloc[0][0].__class__)
print(courses.iloc[0][0])
print(pd.to_datetime(courses.iloc[0][0]))
print(pd.to_datetime(courses.iloc[0][0]).timestamp())
xd0, xd1 = datetime(2015, 1, 1).timestamp(), datetime(2015, 12, 31).timestamp()
orig_axe = plt.gca()
new_axe = orig_axe.twiny()

#new_axe.set_ticklabels([])
new_axe.set_axis_off()
#new_axe.patch.set_visible(False)
#for sp in new_axe.spines.values():
#        sp.set_visible(False)

new_axe.set_xlim(xd0, xd1)
orig_axe.set_ylim(0, None)
new_axe.scatter([d.timestamp() for d in courses['date']], courses['km'],
                 s=50,
                 c='r', # or sequence
                 marker='o',
                 cmap=None, # if c is an array of float
                 )

for i, c in courses.iterrows(): # ça renvoie un tuple
#    print(c)
    plt.text(c['date'].timestamp(), c['km'], c['course'])
#plt.text('2015-04-24', 200, 'bonjour')
#plt.
plt.show()
