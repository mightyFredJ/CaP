# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 13:35:30 2016

@author: FJ221066
"""

import numpy as np
import matplotlib.path as path

def make_bar_path(bins, vals):
    """ crée un diagramme à barres à partir d'une série de points
        pour n points dans x il en faut n-1 dans y
        renvoie le 1er arg à refourguer à matplotlib.patches.PathPatch()
        repris de http://matplotlib.org/users/path_tutorial.html#compound-paths
    """
    if len(bins)-len(vals) != 1:
        raise ValueError("err dans make_bar_path(bins, vals) : "
                "%d points dans bins et %d dans vals\n"
                "    (il doit y en avoir 1 de moins dans vals)" %
                (len(bins), len(vals)))

    left = np.array(bins[:-1])
    right = np.array(bins[1:])
    bottom = np.zeros(len(left))
    top = bottom + vals
    nrects = len(left)

    nverts = nrects*(1+3+1)
    verts = np.zeros((nverts, 2))
    codes = np.ones(nverts, int) * path.Path.LINETO
    codes[0::5] = path.Path.MOVETO
    codes[4::5] = path.Path.CLOSEPOLY
    verts[0::5,0] = left
    verts[0::5,1] = bottom
    verts[1::5,0] = left
    verts[1::5,1] = top
    verts[2::5,0] = right
    verts[2::5,1] = top
    verts[3::5,0] = right
    verts[3::5,1] = bottom
    barpath = path.Path(verts, codes)
    return barpath
