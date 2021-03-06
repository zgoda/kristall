import ast
import codecs
import re
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))


def read(*parts):
    with codecs.open(path.join(here, *parts), 'r') as fp:
        return fp.read()


_version_re = re.compile(r"__version\s+=\s+(.*)")


def find_version(*where):
    return str(ast.literal_eval(_version_re.search(read(*where)).group(1)))


test_reqs = [
    'pytest',
    'pytest-cov',
    'pytest-mock',
]

doc_reqs = [
    'Sphinx',
]

dev_reqs = test_reqs + doc_reqs + [
    'pip',
    'setuptools',
    'wheel',
    'ipython',
    'ipdb',
    'watchdog',
    'flake8',
    'flake8-builtins',
    'flake8-bugbear',
    'flake8-comprehensions',
    'flake8-pytest-style',
    'pep8-naming',
    'dlint',
    'python-dotenv',
    'rstcheck',
]


setup(
    name='kristall',
    description='Lightweight web framework for building APIs and backends',
    version=find_version('src', 'kristall', '_version.py'),
    author='Jarek Zgoda',
    author_email='jarek.zgoda@gmail.com',
    url='https://github.com/zgoda/kristall',
    project_urls={
        'Documentation': 'https://kristall.readthedocs.io/',
        'Source': 'https://github.com/zgoda/kristall',
        'Issues': 'https://github.com/zgoda/kristall/issues',
    },
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires='~=3.7',
    zip_safe=False,
    install_requires=[
        'Werkzeug'
    ],
    extras_require={
        'dev': dev_reqs,
        'docs': doc_reqs,
        'test': test_reqs,
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Typing :: Typed',
    ],
)
