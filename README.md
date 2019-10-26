[![Build Status](https://travis-ci.org/ladybug-tools/honeybee-energy-standards.svg?branch=master)](https://travis-ci.org/ladybug-tools/honeybee-energy-standards)
[![Coverage Status](https://coveralls.io/repos/github/ladybug-tools/honeybee-energy-standards/badge.svg?branch=master)](https://coveralls.io/github/ladybug-tools/honeybee-energy-standards)

[![Python 2.7](https://img.shields.io/badge/python-2.7-green.svg)](https://www.python.org/downloads/release/python-270/) [![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

# honeybee-energy-standards

Honeybee-energy extension for standards, codes, and templates.

All of the data that this module adds to the [honeybee-energy](https://github.com/ladybug-tools/honeybee-energy).lib comes from the
[OpenStudio Standards Gem](https://github.com/NREL/openstudio-standards) and the master
[Google Sheets files](https://drive.google.com/drive/folders/1x7yEU4jnKw-gskLBih8IopStwl0KAMEi)
that possess all of the most recent data. The original sources of this data include the following:

* The US Department of Energy [Commercial Reference Buildings](https://www.energy.gov/eere/buildings/commercial-reference-buildings).
* The [ASHRAE Standard 90.1](https://www.ashrae.org/technical-resources/bookstore/standard-90-1) including all versions from 2004 to the present.
* The [Commercial Buildings Energy Consumption Survey (CBECS)](https://www.eia.gov/consumption/commercial/), specifically for any templates before ASHRAE Standard 90.1 2004.

## Installation
```console
pip install honeybee-energy-standards
```

## QuickStart
```python
import honeybee_energy_standards

```

## [API Documentation](http://ladybug-tools.github.io/honeybee-energy-standards/docs)

## Local Development
1. Clone this repo locally
```console
git clone git@github.com:ladybug-tools/honeybee-energy-standards

# or

git clone https://github.com/ladybug-tools/honeybee-energy-standards
```
2. Install dependencies:
```console
cd honeybee-energy-standards
pip install -r dev-requirements.txt
pip install -r requirements.txt
```

3. Run Tests:
```console
python -m pytests tests/
```

4. Generate Documentation:
```console
sphinx-apidoc -f -e -d 4 -o ./docs ./honeybee_energy_standards
sphinx-build -b html ./docs ./docs/_build/docs
```
