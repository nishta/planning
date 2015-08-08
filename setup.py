# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '0.0.1'

setup(
    name='planning',
    version=version,
    description='Project Management System(PMS)',
    author='nishta',
    author_email='vaiju@nishta.in',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=("frappe",),
)
