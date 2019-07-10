#!/usr/bin/env python
"""
    A setuptools based setup module for boidload project
    Allan Millar
    
    Referenced when making:
    https://packaging.python.org/guides/distributing-packages-using-setuptools/
    https://github.com/pypa/sampleproject
"""
from setuptools import setup, find_packages
from os import path
from io import open

with open("README.rst", "r") as f:
    long_description = f.read()

setup(
    name="boidload",
    version="0.1.0",
    license="NDSU",
    description=("Propogative Problem-Solving" +
                           " Capture Control System"),
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Allan Millar",
    author_email="allanlm05@gmail.com",
    url="https://github.com/travelingnight",
    packages=["boidload"]
    #install_requires=[],
    #scripts=[],
    # Hopefully this allows me to just call "initiate" on the command
    # line and it will run the main function in one.py.
    entry_points={
        "console_scripts": [
            "initiate=one:main",
        ],
    }
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development"
    ]
)
