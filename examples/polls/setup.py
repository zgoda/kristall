import codecs
import re
from os import path

from setuptools import find_packages, setup

# parts below shamelessly stolen from pypa/pip
here = path.abspath(path.dirname(__file__))


def read(*parts):
    with codecs.open(path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version = ['\"]([^'\"]*)['\"]",
        version_file,
        re.M,
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


long_description = read('README.md')

base_reqs = [
    'Kristall',
    'Marshmallow',
    'Pony',
    'python-dotenv',
]

test_reqs = [
    'pytest',
    'pytest-cov',
]

dev_reqs = test_reqs + [
    'pip',
    'setuptools',
    'wheel',
    'ipython',
    'ipdb',
    'watchdog',
    'termcolor',
    'flake8',
    'flake8-builtins',
    'flake8-bugbear',
    'flake8-mutable',
    'flake8-comprehensions',
    'pep8-naming',
    'dlint',
]

setup(
    name='polls',
    version=find_version('src', 'polls', '_version.py'),
    author='Jarek Zgoda',
    author_email='jarek.zgoda@gmail.com',
    description='Polls sample for Kristall application',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=base_reqs,
    tests_require=test_reqs,
    extras_require={
        'dev': dev_reqs,
    },
    entry_points={
        'console_scripts': [
            'polls=polls.cli:main',
        ]
    },
    python_requires='~=3.7',
)
