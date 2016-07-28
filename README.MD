# Marc Extractor

A basic Python package for extracting basic Dublin Core metadata from epubs and generating MARC short records. Has been specifically built for National Library of New Zealand use cases, but over time we hope to make it more generic.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisities

Python and pip. The package has been built with Python 3 and virtualenv.
Please note: this package installs the following dependencies:
lxml (for xml parsing)
nose (for testing)
pymarc (for building MARC records)


### Installing

Make a copy of the project locally

```
git clone [path to project on github]
python setup.py install
```

Change into the marc_extractor directory

```
cd marc_extractor
```

Install the package by executing setup.py

```
python setup.py install
```

And here is a basic demo using the Python Interpreter:
```
$ python
Python 3.4.3 (default, Oct 14 2015, 20:28:29) 
[GCC 4.8.4] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from marc_extractor.epub import epub_to_marc
>>> marc_record = epub_to_marc('path/to/file/test.epub')
>>> print(marc_record)
=LDR  00000nam a22000003i 4500
=005  20160728121637.0
=006  m\\\\\o\\d\\\\\\\\
=007  crmn|nnnana||
=008  160728s\\\\\\\\nz\\\\\\o\\\\\00|\0\\\eng\d
=040  \\$aWN$beng$erda$cWN
=245  00$aSample ePub file -- Title /$cWindows 95 Guy
=264  \1$aWellington :$bFake Publishers, inc., $c2015-11-12

>>> 

```
The MARC record can be added to using the pymarc modules.

## Running the tests

This package uses the nose testing framework, which is installed as part of the package. To run the tests, go to the root directory of the package and type the following command:

```
nosetests
```
This will search for test files in the `tests` subdirectory and run them.


## Authors

* **Sean Mosely* - *Initial work* - [SeanMoselyNLNZ](https://github.com/SeanMoselyNLNZ)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

