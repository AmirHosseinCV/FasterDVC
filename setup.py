from setuptools import setup

setup(
    name='dvc',
    version='0.7.0',
    entry_points={
        'console_scripts': ['dvc=dvc.command_line:main'],
    },
    packages=["dvc"],
    description='fast and easy to use data version controller',
    author='AmirCV',
    license='MIT'
)
