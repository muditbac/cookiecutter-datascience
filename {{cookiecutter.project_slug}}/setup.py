import distutils
from pathlib import Path
from typing import List

from setuptools import setup


setup(
    name='{{cookiecutter.project_slug}}',
    version='{{cookiecutter.project_version}}',
    packages=['{{cookiecutter.project_slug}}'],
    url='{{cookiecutter.project_url}}',
    license='{{cookiecutter.project_license}}',
    author='{{cookiecutter.project_author}}',
    author_email='{{cookiecutter.project_email}}',
    description=''
)
