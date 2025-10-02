#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="tidalplaylist",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "tidalapi",
        "beautifulsoup4",
        "lxml",
    ],
    entry_points={
        "console_scripts": [
            "tidal-login=tidalplaylist.bin.login:main",
            "tidal-playlist=tidalplaylist.bin.playlist:main",
            "tidal-daily=tidalplaylist.bin.daily:main",
        ],
    },
)