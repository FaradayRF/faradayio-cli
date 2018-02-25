import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('faradayio_cli/faradayio_cli.py').read(),
    re.M
    ).group(1)

setup(
    name='faradayio-cli',
    packages=['faradayio_cli'],
    entry_points={
        "console_scripts": ['faradayio-cli = faradayio_cli.faradayio_cli:main']
        },
    version=version,
    description='FaradayRF TUN/TAP adapter command line interface',
    author='FaradayRF',
    author_email='Support@FaradayRF.com',
    url='https://github.com/FaradayRF/faradayio-cli',

    license='GPLv3',

    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Communications :: Ham Radio',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
    ],
)
