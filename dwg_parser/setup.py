# dwg_parser/setup.py
from setuptools import setup, find_packages

setup(
    name="dwg_parser",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "cffi>=1.15.0",
        "ezdxf>=0.18.0",
    ],
    entry_points={
        'console_scripts': [
            'dxf-parser=dwg_parser.dxf_parser:main',
        ],
    },
)