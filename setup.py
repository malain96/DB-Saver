#!/usr/bin/env python3
from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='db_saver',
    version='0.1.0',
    description='DB Saver is a small Python script that I developed to save easily and simply my databases.',
    long_description=readme,
    author='Mathieu Alain',
    author_email='alain.mathieu1996^@gmail.com',
    url='https://github.com/malain96/DB-Saver',
    license=license,
    packages=find_packages(exclude='docs')
)