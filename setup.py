from setuptools import setup, find_packages

setup(
    name='python-statsdtail',
    version='0.1',
    packages=find_packages(exclude=['sample-config']),
    include_package_data=True,
    install_requires=[
        'python-daemon==2.1.2',
        'PyYAML==3.12',
        'statsd==3.2.1',
        'tailhead==1.0.2',
    ],
    extras_require={
            'test': ['nose2'],
    },
    package_data={
            'test_data': ['tests/data/python-statsdtail.yaml'],
    },
    test_suite='nose2.collector.collector',
    url='https://github.com/SUNET/python-statsd-tail',
    license='MIT',
    author='Johan Lundberg',
    author_email='lundberg@sunet.se',
    description='Tail logs and send counts to statsd for matching lines',
    entry_points={
        'console_scripts': [
            'statsdtail=statsdtail.main:main',
        ],
    },
)
