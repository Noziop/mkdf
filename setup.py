from setuptools import setup, find_packages

setup(
    name='mkdf',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'mkdf=mkdf.main:main',
        ],
    },
    install_requires=[
        'Flask',
        'pytest',
        'typer>=0.9.0',
        'pyfiglet>=0.8.0',
        'rich>=13.0.0',
    ],
)
