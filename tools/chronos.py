# encoding: utf8

"""
    fonctions utiles pour la course à pied : manipulation des temps
"""

# ---- python ----
import sys
import doctest
import io
import re
from math import fmod
from datetime import timedelta

# ---- other ----
import pandas as pd

# ---- mine ----

# %% -------------------------------------------------------------------


def tps2hr(tps):
    """
        convertit un chrono (str) en durée (float)
        >>> for t in '01:30:00', '0h0m36', "1°6'36''", '5:0', '3h30':
        ...     print("{t} = {h:g} h".format(t=t, h=tps2hr(t)))
        01:30:00 = 1.5 h
        0h0m36 = 0.01 h
        1°6'36'' = 1.11 h
        5:0 = 0.0833333 h
        3h30 = 3.5 h
    """

    # format avec heure/min/sec
    matcher = re.match(r'(\d+) [hH:°] (\d+) [mM:\'] (\d+) [sS\']*', tps, re.X)
    if matcher != None:
        return float(matcher.group(1)) + float(matcher.group(2))/60. + float(matcher.group(3))/3600.

    # format avec min/sec
    matcher = re.match(r'             (\d+) [mM:\'] (\d+) [sS\']*', tps, re.X)
    if matcher != None:
        return float(matcher.group(1))/60. + float(matcher.group(2))/3600.

    # format avec heure/min
    matcher = re.match(r'             (\d+) [h:] (\d+) [mM\']*', tps, re.X)
    if matcher != None:
        return float(matcher.group(1)) + float(matcher.group(2))/60.

    raise ValueError("Format invalide pour le temps {}".format(tps))


def hr2tps(h):
    """
        convertit une durée (float) en chrono (str)
        >>> for h in 1.54444, 0.2, 0.152, 0.08333:
        ...     print("{h:g} h = {t}".format(h=h, t=hr2tps(h)))
        1.54444 h = 01:32:40
        0.2 h = 00:12:00
        0.152 h = 00:09:07
        0.08333 h = 00:05:00
    """
    secs = round(h * 3600)
    secsrest = fmod(secs, 60)
    mins = (secs - secsrest) / 60
    minsrest = fmod(mins, 60)
    h = (mins - minsrest) / 60

    return "{h:02.0f}:{_m:02.0f}:{_s:02.0f}".format(h=h, _m=minsrest, _s=secsrest)


# %% -------------------------------------------------------------------

def pd_td2hr(*args, **kwargs):
    """
        transforme un timedelta en heures
    """
    return pd.to_timedelta(*args, **kwargs) / pd.Timedelta(hours=1)


def str2td(s):
    """
        transforme une chaine du type 'HH:MM:SS' en timedelta
        >>> delta = td("1:22:33")
        >>> assert delta.seconds == 3600+22*60+33
    """
    tps = [int(e) for e in s.split(':')]
    return timedelta(hours=tps[0], minutes=tps[1], seconds=tps[2])

# %% -------------------------------------------------------------------

if __name__ == "__main__":
    quiet = len(sys.argv) > 1 and '-q' in sys.argv[1]
    if quiet:
        sys.stdout = io.StringIO()

    # ---- do the tests
    opts = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
    (fails, tests) = doctest.testmod(optionflags=opts)
    # ---- done

    sys.stdout = sys.__stdout__  # même si not quiet ça ne coûte rien

    if tests == 0:
        print('no tests in this file')
    elif tests > 0 and fails == 0:  # sinon pas d'affichage c'est pénible
        print('%d tests successfully passed' % tests)
    elif quiet:
        print('%d tests over %d FAILED' % (fails, tests))
