"""A functions module, includes all the standard functions.

Combinatorial - factorial, fibonacci, harmonic, bernoulli...
Elementary - hyperbolic, trigonometric, exponential, floor and ceiling, sqrt...
Special - gamma, zeta,spherical harmonics...
"""
from sympy.core.basic import Basic

import combinatorial
import elementary
import special

from special.polynomials import (legendre, assoc_legendre, hermite, chebyshevt,
        chebyshevu, chebyshevu_root, chebyshevt_root, laguerre_l)

# see #391
from combinatorial.factorials import factorial, factorial2, rf, ff, binomial
from combinatorial.factorials import factorial, RisingFactorial, FallingFactorial
from combinatorial.factorials import binomial, factorial2
from combinatorial.numbers import fibonacci, lucas, harmonic, bernoulli, bell, euler, catalan

from elementary.miscellaneous import sqrt, root, Min, Max, Id, real_root, round
from elementary.complexes import (re, im, sign, Abs, conjugate, arg,
                      polar_lift, periodic_argument, unbranched_argument,
                      principal_branch)
from elementary.trigonometric import acot, cot, tan, cos, sin, asin, acos, atan, atan2
from elementary.exponential import exp_polar, exp, log, LambertW
from elementary.hyperbolic import sinh, cosh, tanh, coth, asinh, acosh, atanh, acoth
from elementary.integers import floor, ceiling
from elementary.piecewise import Piecewise, piecewise_fold

from special.error_functions import erf, Ei, expint, E1, Si, Ci, Shi, Chi
from special.gamma_functions import gamma, lowergamma, uppergamma, polygamma, \
         loggamma, digamma, trigamma, beta
from special.zeta_functions import dirichlet_eta, zeta, lerchphi, polylog
from special.spherical_harmonics import Ylm, Zlm
from special.tensor_functions import Eijk, LeviCivita, KroneckerDelta
from special.delta_functions import DiracDelta, Heaviside
from special.bsplines import bspline_basis, bspline_basis_set
from special.bessel import besselj, bessely, besseli, besselk, hankel1, \
                           hankel2, jn, yn, jn_zeros
from special.hyper import hyper, meijerg

ln = log
