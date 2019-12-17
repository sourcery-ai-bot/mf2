# -*- coding: utf-8 -*-

"""Implementation of the adjustable bi-fidelity Trid function
as defined in:

    Toal, D.J.J. Some considerations regarding the use of multi-
    fidelity Kriging in the construction of surrogate models.
    Struct Multidisc Optim 51, 1223–1245 (2015)
    doi:10.1007/s00158-014-1209-5
"""

from functools import partial

import numpy as np

from mf2.multiFidelityFunction import MultiFidelityFunction


def trid_hf(xx):
    xx = np.atleast_2d(xx)

    temp1 = np.sum((xx - 1) ** 2, axis=1)
    temp2 = np.sum(xx[:,:-1] * xx[:,1:], axis=1)
    return temp1 - temp2

def adjustable_trid_lf(xx, a4):
    xx = np.atleast_2d(xx)

    temp1 = np.sum((xx - a4) ** 2, axis=1)
    temp2 = np.sum((a4-0.65) * xx[:,:-1] * xx[:,1:] * np.arange(2, 11), axis=1)
    return temp1 - temp2


def trid(a4):
    return MultiFidelityFunction(
        f"adjustable Trid {a4}",
        [1]*10, [0]*10,
        [trid_hf, partial(adjustable_trid_lf, a4=a4)],
        fidelity_names=['high', 'low'],
    )
