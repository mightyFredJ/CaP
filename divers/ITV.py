# coding: UTF-8

import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------------------
# données à plotter

data = {
    'UT4M': {
        'kms':  [13.3, 26.8, 35.3, 40.3, 52.4, 61.4, 68.6, 79.2, ],
        'ekmh':  [9.4, 7.2, 7.2, 8.1, 7.8, 6.5, 6.4, 7.1, ],
        'color': 'grey',
    },
    'ITV': {
        'kms':  [20.3, 29.8, 44.5, 56.7, ],
        'ekmh':  [9.1, 8.4, 7.9, 6.8, ],
        'color': 'red',
    },
}

# ----------------------------------------------------------------
# éléments d'analyse

def get_fitted_data(x, y, deg=1):
    """
        fit y :
            renvoie un tableau contenant pour les absisses x 
            les valeurs fittées
        >>> get_fitted_data([0, 1, 2, 3], [1, 2, 2, 1])
        array([ 1.5,  1.5,  1.5,  1.5])
    """
    linfit = np.polyfit(x, y, deg) # tableau de coefs
    poly   = np.poly1d( linfit )   # mise en forme dans un polynôme plus facile à utiliser
    return poly(x)

# mes prévisions optimistes
estim_ekmh_opt = [ 9.0 * (1.-i*0.02) for i in range(len(data['ITV']['ekmh'])) ]
estim_ekmh_pes = [ 8.5 * (1.-i*0.03) for i in range(len(data['ITV']['ekmh'])) ]
    
# ----------------------------------------------------------------
# plot

fig = plt.figure(figsize=(12,6))
plt.subplots_adjust(wspace=0.5)

plt.title('Evolution de la vitesse (corr. du D+)')
plt.grid(True)
plt.xlabel('km')
plt.ylabel('vitesse ((km + D+/100)/h)')

for course in data:
    print(course)
    kms, vits = data[course]['kms'], data[course]['ekmh']
    col = data[course]['color']
    
    # passage en milieux de dist
    kms.insert(0, 0)
    mids = [ (kms[i]+kms[i+1])/2. for i in range(len(kms)-1) ]
    
    # capture du plot pour récupérer sa couleur
    plt.plot(mids, vits, marker='o', ls='', label = course, c=col)
    plt.plot(mids, get_fitted_data(mids, vits), linestyle = "-", linewidth=3, color=col)

    if course == 'ITV':
        plt.plot(mids, estim_ekmh_opt, ls='-.', color=col)
        plt.plot(mids, estim_ekmh_pes, ls='-.', color=col)

plt.legend()

colUT4M = data['UT4M']['color']

# import matplotlib.patches as mpatches
# plt.gca().add_patch( mpatches.Ellipse(xy=(25.5, 7.2), width=17, height=0.5, fill=None, color=colUT4M) )
# plt.gca().annotate("secteur boueux\n= ~ -1 ekm/h",
    # xytext=(15, 6.5), textcoords='data', # départ
    # xy=(20, 7), xycoords='data', # arrivée
    # color=colUT4M,
    # arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color=colUT4M),
# )
# plt.gca().annotate("début de la nuit\n= ~ -1 ekm/h",
    # xytext=(45, 6.25), textcoords='data', # départ
    # xy=(56.5, 6.45), xycoords='data', # arrivée
    # color=colUT4M,
    # arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color=colUT4M),
# )

plt.show()

fig.savefig('ITV_vs_UT4M.png')
