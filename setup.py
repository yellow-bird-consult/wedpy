from setuptools import setup, find_packages


setup(
    name='wedpy',
    version='0.1',
    packages=find_packages(exclude=('tests', 'tests.*', 'tests.*.*')),
    entry_points={
        'console_scripts': [
            # 'halfloop-install = runner.entry_points.install:main',
            # 'halfloop-run = runner.entry_points.run_services:main',
            # 'halfloop-wipe = runner.entry_points.wipe_repos:main',
        ]
    },
    install_requires=[
        'PyYAML==6.0',
    ],
    package_data={'': ['*.yml']}
)