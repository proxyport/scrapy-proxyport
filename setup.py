import os

from setuptools import find_packages, setup


here = os.path.abspath(os.path.dirname(__file__))

NAME = 'scrapyproxyport'
DESCRIPTION = 'Proxy Port integration with Scrapy framework.'
URL = 'https://github.com/proxyport/scrapy-proxyport'
EMAIL = 'proxyportcom@gmail.com'
AUTHOR = 'Proxy Port'
REQUIRES_PYTHON = '>=3.6.0'
README = ''
VERSION = ''

REQUIRED = ['proxyport']

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

with open(os.path.join(here, 'scrapyproxyport', '__version__.py')) as f:
    globs = dict()
    exec(f.read(), globs)
    VERSION = globs['__version__']


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRED,
    url=URL,
    packages=find_packages(exclude=['tests.*']),
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
