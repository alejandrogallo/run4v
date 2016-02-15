from setuptools import setup

import run4v


setup(name="run4v",
    version=run4v.__version__,
    description="A simple and limited VASP runner",
    url="http://github.com/alejandrogallo/run4v",
    author="Alejandro Gallo",
    license="MIT",
    packages=["run4v"],
    test_suite="run4v.tests",
    scripts=["tools/run4v"],
    zip_safe=False)

