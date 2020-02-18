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
```
git clone git@github.com:ladybug-tools/honeybee-energy-standards

# or

git clone https://github.com/ladybug-tools/honeybee-energy-standards
```
2. Install dependencies:
```
cd honeybee-energy-standards
pip install -r dev-requirements.txt
pip install -r requirements.txt
```

3. Run Tests:
```
python -m pytests tests/
```

4. Generate Documentation:
```
sphinx-apidoc -f -e -d 4 -o ./docs ./honeybee_energy_standards
sphinx-build -b html ./docs ./docs/_build/docs
```

5. Re-generate the Data from the [OpenStudio Standards Gem](https://github.com/NREL/openstudio-standards)
(or to update the JSONs based on changes to the honeybee schema)
```
from honeybee_energy_standards._util._all import clean_all, remove_all
from honeybee_energy_standards._util._all import convert_to_hb_json, remove_hb_jsons

remove_hb_jsons()  # remove all of the honeybee JSON data that currently exists

# generate clean OpenStudio Standards Data JSONs from the gem
ashrae_standards = 'C:/Users/chris/Documents/GitHub/openstudio-standards/lib/' \
    'openstudio-standards/standards/ashrae_90_1/'
clean_all(ashrae_standards)

# change the package to load all data from the clean Standards Gem JSONs
import honeybee_energy_standards._change_to_standards_data

convert_to_hb_json()  # generate Honeybee JSONs from the clean Standards Gem JSONs
remove_all()  # remove all of the clean Standards Gem JSONs now that they're converted
```


## Note to developers using this repo as an example
Developers may use this repositiory and Python package as a template to create their
own extensions for the library of standards accessible to honeybee_energy. For such
developers, it is important to know that all of the Python code within the honeybee_energy_standards
package of this repository is not required to make such an extenstion and the only
required folder within the package is the `data` folder. All Python code of this package
only exists to update the JSONs within this `data` folder, which are what actually
extend the `honeybee_energy` package. The `data` folder of any extension must obey
the following rules:

* All JSONs must use the [Honeybee Model Schema](https://www.ladybug.tools/honeybee-schema/model.html)
    representation of objects and must be formatted with the name of the object as keys
    and the schema definition of the object as values.
* The following sub-folders of `data` must be present: `constructions`, `constructionsets`,
    `schedules` and `programtypes`.
* The `constructions` sub-folder should contain the following files: `opaque_material.json`,
    `opaque_construction.json`, `window_material.json`, `window_constructions.json`.
    These files should possess objects that match their names.
* The `schedules` sub-folder should have all schedules in a `schedule.json` file.
* The `constructionsets` and `programtypes` folder can possess any number of JSON
    files with their respective objects.
* The objects that make up larger objects must be present. For example, all of the
    constructions that make up the objects in `constructionsets` must be found in the
    `constructions` sub-folder.
