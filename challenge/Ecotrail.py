#!/usr/bin/python
# -*- coding: UTF-8 -*-
 # ----------------------------------------------------------------

import numpy as np

km  = np.array( [23,   45,   56,   68,   79] )
# classements
csv = np.array( [1343, 1263, 1260, 1166, 1143] )
cfj = np.array( [1626, 1223, 1019, 817, 713] )

# vitesses (pourries)
vsv = np.array( [9.48, 6.72, 6.96, 7.03, 5.79] )
vfj = np.array( [8.65, 7.44, 8.65, 8.36, 7.28] )

# correction des vitesses sur les 2 derniers intervalles
kmerr = np.array( [23,   45,   56,   69,   79] )
def corrige_vitesses( tab ):
    tabcorr = np.array( tab )
    for i in [-2, -1]:
        d = km[i] - km[i-1]
        derr = kmerr[i] - kmerr[i-1]
        verr = tab[i]
        vcorr = float(d) / derr * verr
        # print d, derr, verr, vcorr
        tabcorr[i] = vcorr
    return tabcorr
vfjcorr = corrige_vitesses( vfj )
vsvcorr = corrige_vitesses( vsv )

# print vsv
# print vsvcorr
# print vfj
# print vfjcorr

def get_fitted_data(x, y, deg=1):
    linfit = np.polyfit(x, y, deg) # tableau de coefs
    poly   = np.poly1d( linfit )   # mise en forme dans un polynôme plus facile à utiliser
    return poly(x)

fitsv1 = get_fitted_data(km, vsvcorr)
fitsv2 = get_fitted_data(km[1:], vsvcorr[1:])
fitfj = get_fitted_data(km, vfjcorr, 1) # tableau de coefs

# ----------------------------------------------------------------

import matplotlib.pyplot as plt

fig = plt.figure(figsize=(12,6))
plt.subplots_adjust(wspace=0.5)

plt.subplot(121)
plt.title('Evolution de la vitesse')
plt.grid(True)
plt.xlabel('km')
plt.ylabel('vitesse (km/h)')
_sv = plt.plot(km, vsvcorr, marker='o', label = "Syl20")
plt.plot(km, fitsv1, linestyle = ":", linewidth=3, color = _sv[0].get_color())#color = 'r')
plt.plot(km[1:], fitsv2, linestyle = "dashed", color = _sv[0].get_color())

_fj = plt.plot(km, vfjcorr, marker='o', label = "FredJ")
plt.plot(km, fitfj, marker='x', linestyle = "dashed", color = _fj[0].get_color())
plt.legend()

plt.subplot(122)
plt.title('Evolution du classement')
plt.grid(True)
plt.xlabel('km')
plt.ylabel('position')
plt.plot(km, csv, marker='o', label = "Syl20")
plt.plot(km, cfj, marker='o', label = "FredJ")
plt.legend()
plt.show()

fig.savefig('ProgressionEcotrail.png')
