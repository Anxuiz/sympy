from sympy import Symbol, exp, Integer, Float, sin, cos, log, Poly, Lambda, \
    Function, I, S, sqrt, srepr, Rational, Tuple
from sympy.abc import x, y
from sympy.core.sympify import sympify, _sympify, SympifyError
from sympy.core.decorators import _sympifyit
from sympy.utilities.pytest import XFAIL, raises
from sympy.utilities.decorator import conserve_mpmath_dps
from sympy.geometry import Point, Line
from sympy.functions.combinatorial.factorials import factorial, factorial2

from sympy import mpmath

def test_439():
    v = sympify("exp(x)")
    assert v == exp(x)
    assert type(v) == type(exp(x))
    assert str(type(v)) == str(type(exp(x)))

def test_sympify1():
    assert sympify("x") == Symbol("x")
    assert sympify("   x") == Symbol("x")
    assert sympify("   x   ") == Symbol("x")
    # 1778
    n1 = Rational(1, 2)
    assert sympify('--.5') == n1
    assert sympify('-1/2') == -n1
    assert sympify('-+--.5') == -n1
    assert sympify('-.[3]') == Rational(-1, 3)
    assert sympify('.[3]') == Rational(1, 3)
    assert sympify('+.[3]') == Rational(1, 3)
    assert sympify('+0.[3]*10**-2') == Rational(1, 300)
    assert sympify('.[052631578947368421]') == Rational(1, 19)
    assert sympify('.0[526315789473684210]') == Rational(1, 19)
    assert sympify('.034[56]') == Rational(1711, 49500)
    # options to make reals into rationals
    assert sympify('1.22[345]', rational=1) == \
           1 + Rational(22, 100) + Rational(345, 99900)
    assert sympify('2/2.6', rational=1) == Rational(10, 13)
    assert sympify('2.6/2', rational=1) == Rational(13, 10)
    assert sympify('2.6e2/17', rational=1) == Rational(260, 17)
    assert sympify('2.6e+2/17', rational=1) == Rational(260, 17)
    assert sympify('2.6e-2/17', rational=1) == Rational(26, 17000)
    assert sympify('2.1+3/4', rational=1) == Rational(21, 10) + Rational(3, 4)
    assert sympify('2.234456', rational=1) == Rational(279307, 125000)
    assert sympify('2.234456e23', rational=1) == 223445600000000000000000
    assert sympify('2.234456e-23', rational=1) == Rational(279307, 12500000000000000000000000000)
    assert sympify('-2.234456e-23', rational=1) == Rational(-279307, 12500000000000000000000000000)
    assert sympify('12345678901/17', rational=1) == Rational(12345678901, 17)
    assert sympify('1/.3 + x', rational=1) == Rational(10, 3) + x
    # make sure longs in fractions work
    assert sympify('222222222222/11111111111') == Rational(222222222222, 11111111111)
    # ... even if they come from repetend notation
    assert sympify('1/.2[123456789012]') == Rational(333333333333, 70781892967)
    # ... or from high precision reals
    assert sympify('.1234567890123456', rational=1) == Rational(19290123283179,  156250000000000)

def test_sympify_Fraction():
    try:
        import fractions
    except ImportError:
        pass
    else:
        value = sympify(fractions.Fraction(101, 127))
        assert value == Rational(101, 127) and type(value) is Rational

def test_sympify_gmpy():
    try:
        import gmpy
    except ImportError:
        pass
    else:
        value = sympify(gmpy.mpz(1000001))
        assert value == Integer(1000001) and type(value) is Integer

        value = sympify(gmpy.mpq(101, 127))
        assert value == Rational(101, 127) and type(value) is Rational

@conserve_mpmath_dps
def test_sympify_mpmath():
    value = sympify(mpmath.mpf(1.0))
    assert value == Float(1.0) and type(value) is Float

    mpmath.mp.dps = 12
    assert sympify(mpmath.pi).epsilon_eq(Float("3.14159265359"), Float("1e-12")) is True
    assert sympify(mpmath.pi).epsilon_eq(Float("3.14159265359"), Float("1e-13")) is False

    mpmath.mp.dps = 6
    assert sympify(mpmath.pi).epsilon_eq(Float("3.14159"), Float("1e-5")) is True
    assert sympify(mpmath.pi).epsilon_eq(Float("3.14159"), Float("1e-6")) is False

    assert sympify(mpmath.mpc(1.0 + 2.0j)) == Float(1.0) + Float(2.0)*I

def test_sympify2():
    class A:
        def _sympy_(self):
            return Symbol("x")**3

    a = A()

    assert _sympify(a)== x**3
    assert sympify(a) == x**3
    assert a == x**3

def test_sympify3():
    assert sympify("x**3") == x**3
    assert sympify("x^3") == x**3
    assert sympify("1/2") == Integer(1)/2

    raises(SympifyError, "_sympify('x**3')")
    raises(SympifyError, "_sympify('1/2')")

def test_sympify_keywords():
    raises(SympifyError, "sympify('if')")
    raises(SympifyError, "sympify('for')")
    raises(SympifyError, "sympify('while')")
    raises(SympifyError, "sympify('lambda')")

def test_sympify_float():
    assert sympify("1e-64") != 0
    assert sympify("1e-20000") != 0

def test_sympify_bool():
    """Test that sympify accepts boolean values
    and that output leaves them unchanged"""
    assert sympify(True) == True
    assert sympify(False)== False

def test_sympyify_iterables():
    ans = [Rational(3, 10), Rational(1, 5)]
    assert sympify(['.3', '.2'], rational=1) == ans
    assert sympify(set(['.3', '.2']), rational=1) == set(ans)
    assert sympify(tuple(['.3', '.2']), rational=1) == Tuple(*ans)
    assert sympify(dict(x=0, y=1)) == {x: 0, y: 1}
    assert sympify(['1', '2', ['3', '4']]) == [S(1), S(2), [S(3), S(4)]]

def test_sympify4():
    class A:
        def _sympy_(self):
            return Symbol("x")

    a = A()

    assert _sympify(a)**3== x**3
    assert sympify(a)**3 == x**3
    assert a == x

def test_sympify_text():
    assert sympify('some') == Symbol('some')
    assert sympify('core') == Symbol('core')

    assert sympify('True') == True
    assert sympify('False') == False

    assert sympify('Poly') == Poly
    assert sympify('sin') == sin

def test_sympify_function():
    assert sympify('factor(x**2-1, x)') == -(1-x)*(x+1)
    assert sympify('sin(pi/2)*cos(pi)') == -Integer(1)

def test_sympify_poly():
    p = Poly(x**2+x+1, x)

    assert _sympify(p) is p
    assert sympify(p) is p

def test_sympify_factorial():
    assert sympify('x!') == factorial(x)
    assert sympify('(x+1)!') == factorial(x+1)
    assert sympify('(1 + y*(x + 1))!') == factorial(1 + y*(x + 1))
    assert sympify('(1 + y*(x + 1)!)^2') == (1 + y*factorial(x + 1))**2
    assert sympify('y*x!') == y*factorial(x)
    assert sympify('x!!') == factorial2(x)
    assert sympify('(x+1)!!') == factorial2(x+1)
    assert sympify('(1 + y*(x + 1))!!') == factorial2(1 + y*(x + 1))
    assert sympify('(1 + y*(x + 1)!!)^2') == (1 + y*factorial2(x + 1))**2
    assert sympify('y*x!!') == y*factorial2(x)
    assert sympify('factorial2(x)!') == factorial(factorial2(x))

    raises(SympifyError, 'sympify("+!!")')
    raises(SympifyError, 'sympify(")!!")')
    raises(SympifyError, 'sympify("!")')
    raises(SympifyError, 'sympify("(!)")')
    raises(SympifyError, 'sympify("x!!!")')

def test_sage():
    # how to effectivelly test for the _sage_() method without having SAGE
    # installed?
    assert hasattr(x, "_sage_")
    assert hasattr(Integer(3), "_sage_")
    assert hasattr(sin(x), "_sage_")
    assert hasattr(cos(x), "_sage_")
    assert hasattr(x**2, "_sage_")
    assert hasattr(x+y, "_sage_")
    assert hasattr(exp(x), "_sage_")
    assert hasattr(log(x), "_sage_")

def test_bug496():
    a_ = sympify("a_")
    _a = sympify("_a")

@XFAIL
def test_lambda():
    x = Symbol('x')
    assert sympify('lambda : 1') == Lambda((), 1)
    assert sympify('lambda x: 2*x') == Lambda(x, 2*x)
    assert sympify('lambda x, y: 2*x+y') == Lambda([x, y], 2*x+y)

def test_lambda_raises():
    raises(SympifyError, "_sympify('lambda : 1')")

def test_sympify_raises():
    raises(SympifyError, 'sympify("fx)")')

def test__sympify():
    x = Symbol('x')
    f = Function('f')

    # positive _sympify
    assert _sympify(x)      is x
    assert _sympify(f)      is f
    assert _sympify(1)      == Integer(1)
    assert _sympify(0.5)    == Float("0.5")
    assert _sympify(1+1j)   == 1.0 + I*1.0

    class A:
        def _sympy_(self):
            return Integer(5)

    a = A()
    assert _sympify(a)      == Integer(5)

    # negative _sympify
    raises(SympifyError, "_sympify('1')")
    raises(SympifyError, "_sympify([1,2,3])")


def test_sympifyit():
    x = Symbol('x')
    y = Symbol('y')

    @_sympifyit('b', NotImplemented)
    def add(a, b):
        return a+b

    assert add(x, 1) == x + 1
    assert add(x, 0.5) == x + Float('0.5')
    assert add(x, y) == x + y

    assert add(x, '1') == NotImplemented


    @_sympifyit('b')
    def add_raises(a, b):
        return a+b

    assert add_raises(x, 1) == x + 1
    assert add_raises(x, 0.5) == x + Float('0.5')
    assert add_raises(x, y) == x + y

    raises(SympifyError, "add_raises(x, '1')")

def test_int_float():
    class F1_1(object):
        def __float__(self):
            return 1.1

    class F1_1b(object):
        """
        This class is still a float, even though it also implements __int__().
        """
        def __float__(self):
            return 1.1

        def __int__(self):
            return 1

    class F1_1c(object):
        """
        This class is still a float, because it implements _sympy_()
        """
        def __float__(self):
            return 1.1

        def __int__(self):
            return 1

        def _sympy_(self):
            return Float(1.1)

    class I5(object):
        def __int__(self):
            return 5

    class I5b(object):
        """
        This class implements both __int__() and __float__(), so it will be
        treated as Float in SymPy. One could change this behavior, by using
        float(a) == int(a), but deciding that integer-valued floats represent
        exact numbers is arbitrary and often not correct, so we do not do it.
        If, in the future, we decide to do it anyway, the tests for I5b need to
        be changed.
        """
        def __float__(self):
            return 5.0

        def __int__(self):
            return 5

    class I5c(object):
        """
        This class implements both __int__() and __float__(), but also
        a _sympy_() method, so it will be Integer.
        """
        def __float__(self):
            return 5.0

        def __int__(self):
            return 5

        def _sympy_(self):
            return Integer(5)

    i5 = I5()
    i5b = I5b()
    i5c = I5c()
    f1_1 = F1_1()
    f1_1b = F1_1b()
    f1_1c = F1_1c()
    assert sympify(i5) == 5
    assert isinstance(sympify(i5), Integer)
    assert sympify(i5b) == 5
    assert isinstance(sympify(i5b), Float)
    assert sympify(i5c) == 5
    assert isinstance(sympify(i5c), Integer)
    assert abs(sympify(f1_1) - 1.1) < 1e-5
    assert abs(sympify(f1_1b) - 1.1) < 1e-5
    assert abs(sympify(f1_1c) - 1.1) < 1e-5

    assert _sympify(i5) == 5
    assert isinstance(_sympify(i5), Integer)
    assert _sympify(i5b) == 5
    assert isinstance(_sympify(i5b), Float)
    assert _sympify(i5c) == 5
    assert isinstance(_sympify(i5c), Integer)
    assert abs(_sympify(f1_1) - 1.1) < 1e-5
    assert abs(_sympify(f1_1b) - 1.1) < 1e-5
    assert abs(_sympify(f1_1c) - 1.1) < 1e-5

def test_issue1034():
    a = sympify('Integer(4)')

    assert a == Integer(4)
    assert a.is_Integer

def test_issue883():
    a = [3, 2.0]
    assert sympify(a) == [Integer(3), Float(2.0)]
    assert sympify(tuple(a)) == Tuple(Integer(3), Float(2.0))
    assert sympify(set(a)) == set([Integer(3), Float(2.0)])

def test_S_sympify():
    assert S(1)/2 == sympify(1)/2
    assert (-2)**(S(1)/2) == sqrt(2)*I

def test_issue1689():
    assert srepr(S(1.0+0J)) == srepr(S(1.0)) == srepr(Float(1.0))
    assert srepr(Float(1)) != srepr(Float(1.0))

def test_issue1699_None():
    assert S(None) is None

def test_issue1889_builtins():
    C = Symbol('C')
    vars = {}
    vars['C'] = C
    exp1 = sympify('C')
    assert exp1 == C # Make sure it did not get mixed up with sympy.C

    exp2 = sympify('C', vars)
    assert exp2 == C # Make sure it did not get mixed up with sympy.C

def test_geometry():
    p = sympify(Point(0, 1))
    assert p == Point(0, 1) and type(p) == Point
    L = sympify(Line(p, (1, 0)))
    assert L == Line((0, 1), (1, 0)) and type(L) == Line
