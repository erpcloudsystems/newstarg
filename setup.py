# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in newstareg/__init__.py
from newstareg import __version__ as version

setup(
	name='newstareg',
	version=version,
	description='some ERPNext Customization',
	author='erpcloud.systems',
	author_email='mg@erpcloud.systems',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
