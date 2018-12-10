# brunns-row

Convenience wrapper for DB API and csv.DictReader rows, and similar.

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Build Status](https://travis-ci.org/brunns/brunns-row.svg?branch=master&logo=travis)](https://travis-ci.org/brunns/brunns-row)
[![PyPi Version](https://img.shields.io/pypi/v/brunns-row.svg?logo=pypi)](https://pypi.org/project/brunns-row/#history)
[![Python Versions](https://img.shields.io/pypi/pyversions/brunns-row.svg?logo=python)](https://pypi.org/project/brunns-row/)
[![Licence](https://img.shields.io/github/license/brunns/brunns-row.svg)](https://github.com/brunns/brunns-row/blob/master/LICENSE)
[![GitHub all releases](https://img.shields.io/github/downloads/brunns/brunns-row/total.svg?logo=github)](https://github.com/brunns/brunns-row/releases/)
[![GitHub forks](https://img.shields.io/github/forks/brunns/brunns-row.svg?label=Fork&logo=github)](https://github.com/brunns/brunns-row/network/members)
[![GitHub stars](https://img.shields.io/github/stars/brunns/brunns-row.svg?label=Star&logo=github)](https://github.com/brunns/brunns-row/stargazers/)
[![GitHub watchers](https://img.shields.io/github/watchers/brunns/brunns-row.svg?label=Watch&logo=github)](https://github.com/brunns/brunns-row/watchers/)
[![GitHub contributors](https://img.shields.io/github/contributors/brunns/brunns-row.svg?logo=github)](https://github.com/brunns/brunns-row/graphs/contributors/)
[![GitHub issues](https://img.shields.io/github/issues/brunns/brunns-row.svg?logo=github)](https://github.com/brunns/brunns-row/issues/)
[![GitHub issues-closed](https://img.shields.io/github/issues-closed/brunns/brunns-row.svg?logo=github)](https://github.com/brunns/brunns-row/issues?q=is%3Aissue+is%3Aclosed)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/brunns/brunns-row.svg?logo=github)](https://github.com/brunns/brunns-row/pulls)
[![GitHub pull-requests closed](https://img.shields.io/github/issues-pr-closed/brunns/brunns-row.svg?logo=github)](https://github.com/brunns/brunns-row/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aclosed)

## Setup

Install with pip:

    pip install brunns-row

(As usual, use of a [venv](https://docs.python.org/3/library/venv.html) or [virtualenv](https://virtualenv.pypa.io) is recommended.)

## Developing

Requires [tox](https://tox.readthedocs.io). Run `make precommit` tells you if you're OK to commit. For more options, run:

    make help

## Releasing

Requires [hub](https://hub.github.com/), [setuptools](https://setuptools.readthedocs.io), [wheel](https://pypi.org/project/wheel/) and [twine](https://twine.readthedocs.io). To release `n.n.n`:

    version="n.n.n"
    git commit -am"Release $version" && git push # If not already all pushed, which it should be.
    hub release create $version -m"Release $version"
    python3 setup.py sdist bdist_wheel
    twine upload dist/*$version*
    
Quick version:

    version="n.n.n"
    git commit -am"Release $version" && git push && hub release create $version -m"Release $version" && python setup.py sdist bdist_wheel && twine upload dist/*$version*
