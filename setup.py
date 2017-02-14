from setuptools import setup, find_packages

setup(
    name='python-statsdtail',
    version='0.1.0',
    packages=find_packages(exclude=['sample-config']),
    include_package_data=True,
    install_requires=[
        'python-daemon==2.1.2',
        'PyYAML==3.12',
        'statsd==3.2.1',
        'tailhead==1.0.2',
    ],
    extras_require={
            'test': ['nose'],
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
