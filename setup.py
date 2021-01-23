from setuptools import find_packages, setup

setup(
    name='dvc',
    version='0.3.0',
    scripts=["bin/dvc.bat"],
    packages=find_packages(),
    py_modules=["dvc"],
    description='fast and easy to use data version controller',
    author='AmirCV',
    license='MIT'
)
