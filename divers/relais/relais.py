# encoding utf8

import csv
import pandas as pd
import matplotlib.pyplot as plt

temps = []
with open('Resultats2016.csv') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';')
    csvreader.__next__()
    for row in csvreader:
        t = row[-1].replace("'", ":")
        temps.append('00:' + t)
        # print(t)#', '.join(row))

data = pd.DataFrame(temps, columns=['temps'])
# print(data.head())
data['h'] = pd.to_timedelta(data['temps']) / pd.Timedelta(hours=1)
data['pc'] = data.index / len(data)
print(data.head())
itese = data.iloc[50]
print('itese', itese)

n, bins, patches = plt.hist(data['h'],
                            bins=10, normed=False, histtype='step',
                            label='temps')

def get_y_for_x(x):
    for i in range(len(n)-1):
        if bins[i] < x and x < bins[i+1]:
            return n[i]
    return 0

x, y = itese['h'], get_y_for_x(itese['h'])
plt.scatter(x, y, c='r', s=100)
plt.annotate('DAS/I-tésé', xy=(x, y), xycoords='data',
             xytext=(x-.05, y+1),
             # horizontalalignment='right',
             arrowprops=dict(arrowstyle="->", color='r'),
             color='r',
             )               
from matplotlib.ticker import FuncFormatter
from datetime import time
# x en h mais je veux des hh:mm sur l'axe
def myfmt(x, dummy):
    h = int(x)
    m = int((x - h) * 60)
    return time(hour=h, minute=m).strftime('%H:%M')
plt.gca().xaxis.set_major_formatter(FuncFormatter(myfmt))
plt.ylim(ymin=0)
# plt.legend()
plt.xlabel('Temps')
plt.ylabel('Arrivants')
plt.show()
