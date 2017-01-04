# encoding: utf8

"""
"""

# ---- python ----
#import doctest
#import sys
import re
from datetime import datetime, timedelta

# ---- other ----
import pandas as pd
import matplotlib.pyplot as plt


# ---- mine ----

# %% -------------------------------------------------------------------

plt.xkcd()
pd.set_option('expand_frame_repr', False) # pas de retour à la ligne
pd.options.display.precision = 1 # ou pd.set_option('precision',1)

# %% -------------------------------------------------------------------


regChr = re.compile(r'\d\d:\d\d:\d\d')
durees = pd.DataFrame(columns=['B1/1', 'B1/2', 'B1/3', 'B1/4', 'R', 'B2/1', 'B2/2', 'B2/3', 'B2/4'])
vitess = pd.DataFrame(columns=['B1/1', 'B1/2', 'B1/3', 'B1/4', 'R', 'B2/1', 'B2/2', 'B2/3', 'B2/4'])

dists_tot = [0, 13, 29.5, 46, 56.3, 56.3, 70, 83.8, 103.6, 112]
dists = [dists_tot[i]-dists_tot[i-1] for i in range(1, len(dists_tot))]
print(dists)
#{
#    'B1/1': 13,
#    'B1/2': 29.5,
#    'B1/3': 46,
#    'B1/4': 56.3,
#    'R': 9999,
#    'B2/1': 70,
#    'B2/2': 83.8
#    'B2/3': 103.6,
#    'B2/4': 112,
#}

def timedelta2hoursfloat(*args, **kwargs):
    return pd.to_timedelta(*args, **kwargs) / pd.Timedelta(hours=1)

# %% -------------------------------------------------------------------


with open('origole2016.txt') as finp:
    for line in finp:
        tps = re.findall(regChr, line)
        if len(tps) > 0:
            try:
                # on met le 1er chrono à la fin
                tps = tps[1:] + tps[:1]

                classt, nom = line.split()[0:2]
                if classt.startswith('DNS'):
                    continue
                if classt.startswith('DNF'):
                    continue

                print(classt, nom, len(tps), tps)

                # on calcule les deltas
                deltas = []

                # le 1er
                delt = datetime.strptime(tps[0], '%H:%M:%S')
                delt = timedelta(hours=delt.hour, minutes=delt.minute, seconds=delt.second)
                deltas.append(delt)
                print(' <', deltas[-1], end='>')

                for it in range(1, len(tps)):
                    if it == 4: # gymnase : rien à retoucher
                        delt = datetime.strptime(tps[it], '%H:%M:%S')
                        delt = timedelta(hours=delt.hour, minutes=delt.minute, seconds=delt.second)
                    elif it == 5: # après le gymnase : il faut retirer le gymnase et le cumul précédent
                        strGymn = datetime.strptime(tps[it-1], '%H:%M:%S')
                        deltGymn = timedelta(hours=strGymn.hour, minutes=strGymn.minute, seconds=strGymn.second)
                        delt = datetime.strptime(tps[it], '%H:%M:%S') - datetime.strptime(tps[it-2], '%H:%M:%S')
                        delt -= deltGymn
#                        print()
#                        delt = timedelta(hours=delt.hour, minutes=delt.minute, seconds=delt.second)
                    else:
                        delt = datetime.strptime(tps[it], '%H:%M:%S') - datetime.strptime(tps[it-1], '%H:%M:%S')
                        if delt.days < 0:
                            delt = pd.NaT
                    deltas.append(delt)
                    print(' <', deltas[-1], end='>')
                print()

#                # on calcule l'heure de sortie du gymnase
#                if len(tps) >= 5:
#                    t3 = datetime.strptime(tps[3], '%H:%M:%S')
#                    t4 = datetime.strptime(tps[4], '%H:%M:%S')
#                    t4 = timedelta(hours=t4.hour, minutes=t4.minute, seconds=t4.second)
#                    t4 += t3
#                    tps[4] = t4.strftime('%H:%M:%S')


                # on complète les chronos absents
                if len(tps) < 9:
                    tps += [pd.NaT] * (9-len(tps))
                    deltas += [pd.NaT] * (9-len(deltas))

                vitess.loc[len(vitess)] = [float(dst)/timedelta2hoursfloat(dr) for dr, dst in zip(deltas, dists)]


#                durees.loc[len(durees)] = tps
                durees.loc[len(durees)] = deltas

            except BaseException as ex:
                print()
                print(line, end='')
                print(line.split())
                print(line.split()[0:1])
                raise ex

print(durees.head())
print(durees.tail())

print(vitess.head())
print(vitess.tail())

fig = plt.figure()
#
#for i, interm in enumerate([
##        'B1/1', 'R',
#        'B2/1', 'B2/2',
#        'B2/3', 'B2/4',
#    ]):
#    plt.subplot(2, 2, i+1)
#    dd = timedelta2hoursfloat(durees[interm])
#    #print(dd)
#    plt.hist(dd[dd.notnull()], bins=20)
#    plt.title(interm)
#
#
# n'ont pas coupé :
for i in [0, 44, 139]:#range(len(vitess))[::70]:
#    plt.bar(range(len(vitess.loc[i])), vitess.loc[i], label="%d"%(i+1))
    vits = [0] + list(vitess.loc[i].values) + [0]
    plt.step(dists_tot + [dists_tot[-1]], vits, label="%d"%(i+1), lw=2)
plt.legend()
plt.ylim(ymin=5, ymax=13)
plt.xlabel('km')
plt.ylabel('km/h')
plt.show()

# ont coupé :
for i in [11, 79]:
    vits = [0] + list(vitess.loc[i].values) + [0]
    plt.step(dists_tot + [dists_tot[-1]], vits, label="%d"%(i+1), lw=2)
plt.legend()
plt.ylim(ymin=4)
plt.xlabel('km')
plt.ylabel('km/h')
plt.show()

## pas sûr...
#for i in range(2, 10):#[0, 40, 70, 140]:#range(len(vitess))[::70]:
##    plt.bar(range(len(vitess.loc[i])), vitess.loc[i], label="%d"%(i+1))
##    print(len(dists_tot), dists_tot)
#    vits = [0] + list(vitess.loc[i].values) + [0]
##    print(type(vits), vits)
##    print((0,) + vitess.loc[i].values)
##    print(len([0] + vitess.loc[i].values), [0] + vitess.loc[i].values)
#    plt.step(dists_tot + [dists_tot[-1]], vits, label="%d"%(i+1))
#plt.legend()
#plt.show()

ratio = vitess['B2/2'] / vitess['B2/1']
suspects = ratio[ratio>1.1]
print(len(suspects), 'suspects:', suspects)
print('moi:', ratio.loc[139])
plt.hist(ratio)
plt.xlabel('rapport des vitesses (B2 - 2ème secteur)/(B2 - 1er secteur)')
plt.ylabel('nombre de coureurs')
plt.show()
