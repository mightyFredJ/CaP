# encoding: utf8

"""
    fonctions utiles pour la course à pied
"""

# ---- python ----
import sys
import doctest
import io
import re
from math import fmod
from datetime import datetime

# ---- other ----

# ---- mine ----

# %% -------------------------------------------------------------------

def ekm(km, deniv):
    """ calcule la difficulté d'une course
        >>> ekm(112, 2800)
        140.0
        >>> ekm(100, 2222)
        122.22
    """
    return km + deniv/100.

# %% -------------------------------------------------------------------

def str2dt(s, an=2017):
    """ raccourci vers strptime pour convertir une str en datetime
        >>> str2dt('6/2')
        datetime.datetime(2017, 2, 6, 0, 0)
        >>> str2dt('6/2', 16)
        datetime.datetime(2016, 2, 6, 0, 0)
        >>> str2dt('6/2', 2016)
        datetime.datetime(2016, 2, 6, 0, 0)
    """
    if an > 2000: an -= 2000
    return datetime.strptime(s + '/' + str(an), '%d/%m/%y')


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
