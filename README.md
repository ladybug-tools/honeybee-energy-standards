[![Build Status](https://travis-ci.org/ladybug-tools/honeybee-standards.svg?branch=master)](https://travis-ci.org/ladybug-tools/honeybee-standards)
[![Coverage Status](https://coveralls.io/repos/github/ladybug-tools/honeybee-standards/badge.svg?branch=master)](https://coveralls.io/github/ladybug-tools/honeybee-standards)

[![Python 2.7](https://img.shields.io/badge/python-2.7-green.svg)](https://www.python.org/downloads/release/python-270/) [![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

# honeybee-standards

Honeybee-energy extension for standards, codes, and templates

## Installation
```console
pip install honeybee-standards
```

## QuickStart
```python
import honeybee_standards

```

## [API Documentation](http://ladybug-tools.github.io/honeybee-standards/docs)

## Local Development
1. Clone this repo locally
```console
git clone git@github.com:ladybug-tools/honeybee-standards

# or

git clone https://github.com/ladybug-tools/honeybee-standards
```
2. Install dependencies:
```console
cd honeybee-standards
pip install -r dev-requirements.txt
pip install -r requirements.txt
```

3. Run Tests:
```console
python -m pytests tests/
```

4. Generate Documentation:
```console
sphinx-apidoc -f -e -d 4 -o ./docs ./honeybee_standards
sphinx-build -b html ./docs ./docs/_build/docs
```
