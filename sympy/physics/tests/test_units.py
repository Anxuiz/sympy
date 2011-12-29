from sympy import integrate, Rational, sqrt, Symbol
from sympy.physics.units import (au, charge, day, find_unit, foot, km, m,
                                 meter, minute, s, speed_of_light)

def test_units():
    assert (5*m/s * day) / km == 432
    assert foot / meter == Rational('0.3048')

    # Light from the sun needs about 8.3 minutes to reach earth
    t = (1*au / speed_of_light).evalf() / minute
    assert abs(t - 8.31) < 0.1

    assert sqrt(m**2) == m
    assert (sqrt(m))**2 == m

    t = Symbol('t')
    assert integrate(t*m/s,(t, 1*s, 5*s)) == 12*m*s
    assert (t * m/s).integrate((t, 1*s, 5*s)) == 12*m*s

def test_issue_2466():
    assert (m < s).is_Relational

def test_find_unit():
    assert find_unit('charge') == ['charge']
    assert find_unit(charge) == ['C', 'charge', 'coulomb', 'coulombs']
