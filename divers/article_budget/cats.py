#import pandas as pd
#import numpy as np
#from collections import OrderedDict
#
#from bokeh.sampledata.olympics2014 import data
#from bokeh.charts import Donut
#from bokeh.plotting import show, output_file
#
## we throw the data into a pandas df
#df = pd.io.json.json_normalize(data['data'])
## filter by countries with at least one medal and sort
#df = df[df['medals.total'] > 8]
#df = df.sort("medals.total", ascending=False)
#
## then, we get the countries and we group the data by medal type
#countries = df.abbr.values.tolist()
#gold = df['medals.gold'].astype(float).values
#silver = df['medals.silver'].astype(float).values
#bronze = df['medals.bronze'].astype(float).values
#
## later, we build a dict containing the grouped data
#medals = OrderedDict()
#medals['bronze'] = bronze
#medals['silver'] = silver
#medals['gold'] = gold
#
## any of the following commented are valid Donut inputs
## medals = list(medals.values())
## medals = np.array(list(medals.values()))
## medals = pd.DataFrame(medals)
#output_file("donut.html")
#donut = Donut(medals, countries, filename="donut.html")
#show(donut) # or donut.show()

import matplotlib.pyplot as plt
from matplotlib import colors
plt.figure(figsize=(7, 7))

from collections import OrderedDict
depenses = OrderedDict()
depenses['Chauss.']= 150
depenses['Vêtements']=	 179
depenses['Matériel']=	 192
depenses['Club']=	        32
depenses['Courses']=    498
depenses['Transport']=	 419
depenses['Hébergt.']=233

depcols = ['navy', 'blue', 'royalblue',
           'lightsalmon', 'tomato',
           'darkgreen', 'limegreen',]

x, y = list(depenses.values()), list(depenses.keys())
plt.pie(x, labels=y, colors=depcols, autopct='%d %%', pctdistance=0.8)

categories = OrderedDict()
categories['Equipement']= 150+179+192
categories['Inscriptions']= 32+498
categories['Logistique']=419+233

x, y = list(categories.values()), list(categories.keys())
plt.pie(x, labels=y, radius=0.6, colors=['b', 'r', 'g'], labeldistance=0.25,
        textprops={'color': 'k', 'fontsize': 12, 'backgroundcolor': 'w'})

plt.savefig('cats.png')
plt.show()
