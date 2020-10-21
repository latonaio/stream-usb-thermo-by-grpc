# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

from setuptools import find_packages, setup


setup(
    name="thermo-client",
    version="0.0.1",
    author="Latona",
    packages=find_packages("./client"),
    package_dir={"": "client"},
    install_requires=[],
    tests_require=[]
)
