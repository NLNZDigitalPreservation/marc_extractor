# Marc Extractor

A basic Python package for extracting basic Dublin Core metadata from epubs and generating MARC short records. Has been specifically built for National Library of New Zealand use cases, but over time we hope to make it more generic.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisities

Python and pip. The package has been built with Python 3 and virtualenv.


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

Install the package by calling setup.py

```
python setup.py install
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

This package uses the nose testing framework, which is installed as part of the package. To run the tests, go to the root directory of the package and type the following command:

```
nosetests
```
This will search for test files in the `tests` subdirectory and run them.


## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.


## Authors

* **Sean Mosely* - *Initial work* - [PurpleBooth](https://github.com/JohnnyFalvo)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

