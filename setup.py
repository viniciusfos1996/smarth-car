from setuptools import setup, find_packages

requirements = ["ipython>=6", "nbformat>=4", "nbconvert>=5", "requests>=2"]

setup(
    name='smarth-car',
    version='0.0.1',
    author='Una Classmates',
    description='A project to make a car a little smarth',
    url='https://github.com/1ChristianAlex/smarth-car.git',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
