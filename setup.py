#!/usr/bin/env python
"""Distutils based setup script for SymPy.

This uses Distutils (http://python.org/sigs/distutils-sig/) the standard
python mechanism for installing packages. For the easiest installation
just type the command (you'll probably need root privileges for that):

    python setup.py install

This will install the library in the default location. For instructions on
how to customize the install procedure read the output of:

    python setup.py --help install

In addition, there are some other commands:

    python setup.py clean -> will clean all trash (*.pyc and stuff)
    python setup.py test  -> will run the complete test suite
    python setup.py bench -> will run the complete benchmark suite
    python setup.py audit -> will run pyflakes checker on source code

To get a full list of avaiable commands, read the output of:

    python setup.py --help-commands

Or, if all else fails, feel free to write to the sympy list at
sympy@googlegroups.com and ask for help.
"""

from distutils.core import setup
from distutils.core import Command
import sys
import subprocess
import os

import sympy

# Make sure I have the right Python version.
if sys.version_info[:2] < (2,5):
    print "Sympy requires Python 2.5 or newer. Python %d.%d detected" % \
          sys.version_info[:2]
    sys.exit(-1)

# Check that this list is uptodate against the result of the command:
# $ for i in `find sympy -name __init__.py | rev | cut -f 2- -d '/' | rev | egrep -v "^sympy$" `; do echo "'${i//\//.}',"; done | sort
modules = [
    'sympy.assumptions',
    'sympy.assumptions.handlers',
    'sympy.combinatorics',
    'sympy.concrete',
    'sympy.core',
    'sympy.external',
    'sympy.functions',
    'sympy.functions.combinatorial',
    'sympy.functions.elementary',
    'sympy.functions.special',
    'sympy.galgebra',
    'sympy.geometry',
    'sympy.integrals',
    'sympy.interactive',
    'sympy.logic',
    'sympy.logic.algorithms',
    'sympy.logic.utilities',
    'sympy.matrices',
    'sympy.matrices.expressions',
    'sympy.mpmath',
    'sympy.mpmath.calculus',
    'sympy.mpmath.functions',
    'sympy.mpmath.libmp',
    'sympy.mpmath.matrices',
    'sympy.mpmath.tests',
    'sympy.ntheory',
    'sympy.parsing',
    'sympy.physics',
    'sympy.physics.mechanics',
    'sympy.physics.quantum',
    'sympy.plotting',
    'sympy.polys',
    'sympy.polys.domains',
    'sympy.printing',
    'sympy.printing.pretty',
    'sympy.series',
    'sympy.simplify',
    'sympy.solvers',
    'sympy.statistics',
    'sympy.tensor',
    'sympy.utilities',
    'sympy.utilities.mathml',
  ]

class audit(Command):
    """Audits Sympy's source code for following issues:
        - Names which are used but not defined or used before they are defined.
        - Names which are redefined without having been used.
    """

    description = "Audit Sympy source with PyFlakes"
    user_options = []

    def initialize_options(self):
        self.all = None

    def finalize_options(self):
        pass

    def run(self):
        import os
        try:
            import pyflakes.scripts.pyflakes as flakes
        except ImportError:
            print """In order to run the audit, you need to have PyFlakes installed."""
            sys.exit(-1)
        # We don't want to audit external dependencies
        ext = ('mpmath',)
        dirs = (os.path.join(*d) for d in \
                        (m.split('.') for m in modules) if d[1] not in ext)
        warns = 0
        for dir in dirs:
            for filename in os.listdir(dir):
                if filename.endswith('.py') and filename != '__init__.py':
                    warns += flakes.checkPath(os.path.join(dir, filename))
        if warns > 0:
            print ("Audit finished with total %d warnings" % warns)

class clean(Command):
    """Cleans *.pyc and debian trashs, so you should get the same copy as
    is in the VCS.
    """

    description = "remove build files"
    user_options = [("all","a","the same")]

    def initialize_options(self):
        self.all = None

    def finalize_options(self):
        pass

    def run(self):
        import os
        os.system("py.cleanup")
        os.system("rm -f python-build-stamp-2.4")
        os.system("rm -f MANIFEST")
        os.system("rm -rf build")
        os.system("rm -rf dist")
        os.system("rm -rf doc/_build")


class test_sympy(Command):
    """Runs all tests under the sympy/ folder
    """

    description = "run all tests and doctests; also see bin/test and bin/doctest"
    user_options = []  # distutils complains if this is not here.

    def __init__(self, *args):
        self.args = args[0] # so we can pass it to other classes
        Command.__init__(self, *args)

    def initialize_options(self):  # distutils wants this
        pass

    def finalize_options(self):    # this too
        pass

    def run(self):
        tests_successful = True

        try:
            if not sympy.test():
                # some regular test fails, so set the tests_successful
                # flag to false and continue running the doctests
                tests_successful = False

            if not sympy.doctest():
                tests_successful = False

            print
            sys.path.append("examples")
            from all import run_examples # examples/all.py
            if not run_examples(quiet=True):
                tests_successful = False

            print
            sys.path.append("examples")
            from all import run_examples # examples/all.py
            if not run_examples(quiet=True):
                tests_successful = False

            if not sys.platform == "win32":
                dev_null = open(os.devnull, 'w')
                if subprocess.call("sage -v", shell = True, stdout = dev_null, stderr = dev_null) == 0:
                    if subprocess.call("sage -python bin/test sympy/external/tests/test_sage.py", shell = True) != 0:
                        tests_successful = False

            if tests_successful:
                return
            else:
                # Return nonzero exit code
                sys.exit(1)
        except KeyboardInterrupt:
            print
            print("DO *NOT* COMMIT!")
            sys.exit(1)


class run_benchmarks(Command):
    """Runs all SymPy benchmarks"""

    description = "run all benchmarks"
    user_options = []  # distutils complains if this is not here.

    def __init__(self, *args):
        self.args = args[0] # so we can pass it to other classes
        Command.__init__(self, *args)

    def initialize_options(self):  # distutils wants this
        pass

    def finalize_options(self):    # this too
        pass

    # we use py.test like architecture:
    #
    # o collector   -- collects benchmarks
    # o runner      -- executes benchmarks
    # o presenter   -- displays benchmarks results
    #
    # this is done in sympy.utilities.benchmarking on top of py.test
    def run(self):
        from sympy.utilities import benchmarking
        benchmarking.main(['sympy'])


# Check that this list is uptodate against the result of the command:
# $ python bin/generate_test_list.py
tests = [
    'sympy.assumptions.tests',
    'sympy.combinatorics.tests',
    'sympy.concrete.tests',
    'sympy.core.tests',
    'sympy.external.tests',
    'sympy.functions.combinatorial.tests',
    'sympy.functions.elementary.tests',
    'sympy.functions.special.tests',
    'sympy.galgebra.tests',
    'sympy.geometry.tests',
    'sympy.integrals.tests',
    'sympy.logic.tests',
    'sympy.matrices.expressions.tests',
    'sympy.matrices.tests',
    'sympy.mpmath.tests',
    'sympy.ntheory.tests',
    'sympy.parsing.tests',
    'sympy.physics.quantum.tests',
    'sympy.physics.tests',
    'sympy.plotting.tests',
    'sympy.polys.tests',
    'sympy.printing.pretty.tests',
    'sympy.printing.tests',
    'sympy.series.tests',
    'sympy.simplify.tests',
    'sympy.slow_tests',
    'sympy.solvers.tests',
    'sympy.statistics.tests',
    'sympy.tensor.tests',
    'sympy.utilities.tests',
    ]

classifiers = [
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Scientific/Engineering :: Physics',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.5',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    ]

long_description = '''SymPy is a Python library for symbolic mathematics. It aims
to become a full-featured computer algebra system (CAS) while keeping the code
as simple as possible in order to be comprehensible and easily extensible.
SymPy is written entirely in Python and does not require any external libraries.'''

setup(
      name = 'sympy',
      version = sympy.__version__,
      description = 'Computer algebra system (CAS) in Python',
      long_description = long_description,
      author = 'SymPy development team',
      author_email = 'sympy@googlegroups.com',
      license = 'BSD',
      keywords = "Math CAS",
      url = 'http://code.google.com/p/sympy',
      packages = ['sympy'] + modules + tests,
      scripts = ['bin/isympy'],
      ext_modules = [],
      package_data = { 'sympy.utilities.mathml' : ['data/*.xsl'] },
      data_files = [('share/man/man1', ['doc/man/isympy.1'])],
      cmdclass    = {'test': test_sympy,
                     'bench': run_benchmarks,
                     'clean': clean,
                     'audit' : audit,
                     },
      classifiers = classifiers,
      )
