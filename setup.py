from setuptools import setup, find_packages


setup(
    name='wedpy',
    version='0.1',
    packages=find_packages(exclude=('tests', 'tests.*', 'tests.*.*')),
    entry_points={
        'console_scripts': [
            'wedpy-teardown = wedpy.endpoints.teardown:main',
            'wedpy-stop = wedpy.endpoints.stop:main',
            'wedpy-install = wedpy.endpoints.install:main',
            'wedpy-run = wedpy.endpoints.run:main',
            'wedpy-build = wedpy.endpoints.build:main',
            'wedpy-wipe = wedpy.endpoints.wipe_images:main',
        ]
    },
    install_requires=[
        'PyYAML==6.0',
        'docker==6.0.1'
    ],
    package_data={'': ['*.yml']}
)
