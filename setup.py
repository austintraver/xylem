from setuptools import setup

setup(
    name='xylem',
    version='0.0.1',
    packages=['xylem'],
    entry_points={
        'console_scripts': [
            'xylem=xylem.__main__:run'
        ]
    }
)
