from setuptools import setup

setup(name="run4v",
    version="0.0.1",
    description="A simple and limited VASP runner",
    url="http://github.com/alejandrogallo/run4v",
    author="Alejandro Gallo",
    license="MIT",
    packages=["run4v"],
    test_suite="run4v.tests",
    scripts=["tools/run4v"],
    zip_safe=False)

#tests_require=["nose"],
