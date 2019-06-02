# Copyright 2019 Jarek Zgoda. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from os import path
import re

from setuptools import setup, find_packages

PKG_NAME = 'kristall'


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def get_metadata():
    metadata_file = path.join(here, 'src', PKG_NAME, '_metadata.py')
    with open(metadata_file) as fp:
        content = fp.read()
        return dict(re.findall(r"__([a-z]+)__\s*=\s*'([^']+)'", content))


metadata = get_metadata()


setup(
    name=PKG_NAME,
    description=metadata['description'],
    version=metadata['version'],
    author=metadata['author'],
    author_email=metadata['authoremail'],
    url=metadata['url'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires='~=3.5',
    zip_safe=False,
    install_requires=[
        'Werkzeug',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
    ]
)
