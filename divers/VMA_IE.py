# encoding: utf8

"""
"""

# ---- python ----
#import sys
#import doctest
#from datetime import datetime, timedelta

# ---- other ----
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ---- mine ----
from CaP.tools.chronos import hr2tps, pd_td2hr

# %% -------------------------------------------------------------------

kkms, ktps, kkmh, kVO2, kpcVO2, kkeep = 'kms', 'tps', 'kmh', 'VO2', '%VO2max', 'keep'

refs = (
    ( 1.5, '00:05:09', 1994, False),
    ( 1.6, '00:05:53', 2016, False),
    ( 2.0, '00:07:29', 2015, True),
    ( 5.0, '00:20:25', 2012, False),
    (10.0, '00:40:27', 2016, True),
    (21.1, '01:29:53', 2016, True),
    (21.1, '01:29:06', 2016, True),
    (42.2, '03:20:47', 2009, False),
)
dists = [r[0] for r in refs]
tps = [r[1] for r in refs]
keep = [r[3] for r in refs]


data = pd.DataFrame({
    kkms: dists,
    ktps: tps,
    kkeep: keep,
})

data[kkmh] = data[kkms] / pd_td2hr(data[ktps])
data[kVO2] = data[kkmh] * 3.5
VO2max = data[kVO2][0]
data[kpcVO2] = data[kVO2] / VO2max * 100

print(data.head())

subdata = pd.DataFrame(data[data[kkeep] == True])
print(subdata.head())

# %% -------------------------------------------------------------------

def calc_fit(x, y, deg=1):
    linfit = np.polyfit(x, y, deg) # tableau de coefs
    poly   = np.poly1d( linfit )   # mise en forme dans un polynôme plus facile à utiliser
    print(linfit, poly)
    return poly

def get_fitted_data(x, y, deg=1):
    poly = calc_fit(x, y, deg)
    return poly(x)

fit = calc_fit(np.log(data[kkms]), data[kpcVO2])
fit2 = calc_fit(np.log(subdata[kkms]), subdata[kpcVO2])

xr = [1.1, 60]
fitted = fit(np.log(xr))
fitted2 = fit2(np.log(xr))

pcVMA42 = fit2(np.log(42.2))
V42 = pcVMA42 * data[kkmh][0] / 100.
print('VMA(marath.) = %g' % V42)
dur42 = 42.2 / V42
print('soit', hr2tps(dur42))

fig = plt.figure()
plt.plot(data[kkms], data[kpcVO2], '-o')
plt.plot(xr, fitted, '-')
plt.plot(xr, fitted2, '--')
plt.semilogx()
#plt.xlim(xmin=0, xmax=25)
#plt.ylim(ymin=0, ymax=20)

plt.show()

# %% -------------------------------------------------------------------
