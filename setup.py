# -*- mode: python; coding: utf-8; -*-

from setuptools import setup, find_packages
import os

package = 'migselsim'

def get_metadata(lines):
    data = {}
    for line in lines:
        key, value = line.split('=', 1)
        key = key.strip('_ ')
        value = value.strip()
        data[key] = value
    return data


with open(os.path.join(packagename, 'metadata.py'), 'r') as f:
    metadata = get_metadata(f.readlines[1:])

here = os.path.abspath(os.path.dirname(__file__))
long_description = open(os.path.join(here, 'README.rst')).read()

setup(
    name = package,
    version = metadata['version']
    author = metadata['author']
    author_email = metadata['email'],
    packages = find_packages(),
    license = metadata['license'],
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
