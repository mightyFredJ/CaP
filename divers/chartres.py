# encoding: utf8

"""
"""

# ---- python ----
import re
from datetime import datetime, timedelta
from collections import defaultdict
from pprint import pprint

# ---- other ----
#import pandas as pd
import matplotlib.pyplot as plt

# ---- mine ----

# %% -------------------------------------------------------------------

plt.xkcd()
#pd.set_option('expand_frame_repr', False) # pas de retour à la ligne
#pd.options.display.precision = 1 # ou pd.set_option('precision',1)

# %% -------------------------------------------------------------------

def timedelta2hoursfloat(*args, **kwargs):
    return pd.to_timedelta(*args, **kwargs) / pd.Timedelta(hours=1)

def temps_2_heures(tps):
    import re

    matcher = re.match(r'(\d+) [hH:°] (\d+) [mM:\'] (\d+) [sS\']*', tps, re.X)
    if matcher != None:
        return float(matcher.group(1)) + float(matcher.group(2))/60. + float(matcher.group(3))/3600.

    matcher = re.match(r'             (\d+) [mM:\'] (\d+) [sS\']*', tps, re.X)
    if matcher != None:
        return float(matcher.group(1))/60. + float(matcher.group(2))/3600.
    else:
        raise ValueError("Format invalide pour le temps {}".format(tps))


def heures_2_temps(h):
    """
        >>> for h in 1.54444, 0.2, 0.152, 0.08333:
        ...     print( h, heures_2_temps(h))
        1.54444 01:32:39
        0.2 00:12:00
        0.152 00:0907
        0.08333 00:04:59
    """
    from math import fmod
    secs = h * 3600
    secsrest = fmod(secs, 60)
    mins = (secs - secsrest) / 60
    minsrest = fmod(mins, 60)
    h = (mins - minsrest) / 60

    return "{h:02.0f}:{_m:02.0f}:{_s:02.0f}".format(h=h, _m=minsrest, _s=secsrest)


# %% -------------------------------------------------------------------

regPerf = re.compile(r'\d+ \s+ (\d\d:\d\d:\d\d) .*? ([MF]) \s \( \d+ \s / \s \d+\) \s (\d{6,7}\s)? (.*)? \s \+\d+:\d+:\d+', re.I | re.X)

clubsMix = defaultdict(list)
clubsFex = defaultdict(list)

with open('chartres.txt') as finp:
    for line in finp:
        matched = regPerf.match(line)
        if matched:
#            print(matched.groups())
            (chrono, sexe, license, club) = matched.groups()
            clubsMix[club].append(temps_2_heures(chrono))
            if sexe is 'F':
                clubsFex[club].append(temps_2_heures(chrono))

#pprint(clubs)
clubsFex['AS CEA SACLAY'].append(temps_2_heures('01:50:00'))

challengeMix = {}
for club, chronos in clubsMix.items():
    if len(chronos) < 3:
        continue
    else:
        challengeMix[club] = sum(chronos[:3])

challengeFem = {}
for club, chronos in clubsFex.items():
    if len(chronos) < 3:
        continue
    else:
        challengeFem[club] = sum(chronos[:3])

print('Mixte :')
#pprint(challengeMix)

for club in sorted(challengeMix, key=lambda a: challengeMix[a])[:20]:
    print("{0:<30s} {1:s}".format(club, heures_2_temps(challengeMix[club])))

print("Féminin :")
#pprint(challengeFem)

for club in sorted(challengeFem, key=lambda a: challengeFem[a])[:20]:
    print("{0:<30s} {1:s}".format(club, heures_2_temps(challengeFem[club])))

# %% -------------------------------------------------------------------

