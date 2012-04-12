# -*- mode: python; coding: utf-8; -*-

from setuptools import setup, find_packages
import os

version = '0.0.1'
here = os.path.abspath(os.path.dirname(__file__))
long_description = open(os.path.join(here, 'README.rst')).read()

setup(
    name = 'migselsim',
    version = version,
    author = 'Seiji Kumagai',
    author_email = 'seiji.kumagai@gmail.com',
    packages = find_packages(),
    license = 'LICENSE.txt',
    description = 'Population genetic simulator for sex-specific migration.',
    long_description = long_description,
    install_requires = [
        'simuPOP >= 1.0.7',
        'PyYAML >= 3.10',
        'distribute'
        ],
    entry_points = dict(console_scripts = ['migselsim=migselsim:main']),
    setup_requires = ['nose', 'pinocchio', 'figleaf', 'coverage'],
    zip_safe = False,
    )
