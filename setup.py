try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'My Project',
    'author': 'My Name',
    'url': 'URL to get at it',
    'download_url': 'Where to download it',
    'author_email': 'My email',
    'version': '0.1',
    'install_requires': ['lxml', 'nose', 'pymarc'],
    'packages': ['marc_extractor'],
    'py_modules': ['epub', 'nlnz_epub'],
    'name': 'marc_extractor'
}

setup(**config)
