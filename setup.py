from setuptools import setup, find_packages

version = '0.1.0'

requires = [
    'python-daemon==2.1.2',
    'PyYAML==5.4',
    'statsd==3.2.1',
    'tailhead==1.0.2',
]

testing_requires = [
    'nose',
    'coverage',
    'nosexcover',
]

setup(
    name='python-statsdtail',
    version='0.1.0',
    packages=find_packages(exclude=['sample-config']),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    test_require=testing_requires,
    test_suite='statsdtail',
    extras_require={
        'testing': testing_requires
    },
    package_data={
            'test_data': ['tests/data/python-statsdtail.yaml'],
    },
    url='https://github.com/SUNET/python-statsdtail',
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
