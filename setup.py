# setup.py

from setuptools import setup, find_packages

setup(
    name="event_study",
    version="0.1.0",
    author="LING YUAN",
    author_email="LingYUAN1201@outlook.com",
    description="A Python package for conducting event studies with CAR and AR calculations.",
     packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'statsmodels',
        'scipy',
        'matplotlib',
        'seaborn',
        'openpyxl',
        'xlsxwriter'
    ],
    python_requires='>=3.7',
)
