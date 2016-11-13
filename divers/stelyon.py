# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 21:01:19 2015

@author: FJ221066
"""

# cd c:/Users/fj221066/Documents/Dev/CaP/perso/
import pandas as pd
import matplotlib.pyplot as plt
xl = pd.ExcelFile("Resultats.xlsx")

for page in xl.sheet_names:
    data = xl.parse(sheetname=page,
                    converters={'temps': lambda x: str(x)},
#                    index_col=0,
                    parse_cols="A,E:G")
    data['h'] = pd.to_timedelta(data['temps']) / pd.Timedelta(hours=1)
    data['pc'] = data.index / len(data)
    print(data.head())
    print(data['h'].describe())

#    plt.plot(data['pc'], data['h'])
#    data['h'].hist(bins=20)
    plt.hist(data['h'], bins=15, normed=True, histtype='step',
             label=page)
    #, cumulative=True)

plt.legend()
#data['h'].plot()
#data['h'].hist(bins=20)
