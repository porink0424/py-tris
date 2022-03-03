from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(
        ["lib/constants/*.py", "lib/classes/*.py", "lib/helpers/*.py", "boardWatcher.py", "evaluator.py", "gameStateManager.py", "minoMover.py", "decisionMaker.py"],
        compiler_directives={'language_level' : "3"}
    )
)