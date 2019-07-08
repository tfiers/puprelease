# Puprelease

Publishing a new version of your Python package has never been easier:

![Screencast of pup making a new release](https://raw.githubusercontent.com/tfiers/puprelease/master/example.gif)


## Installation
```
$ pip install puprelease
```
This will get you the
[![latest version on PyPI](https://img.shields.io/pypi/v/puprelease.svg?label=latest%20version%20on%20PyPI:)](https://pypi.python.org/pypi/puprelease/)

## Usage
In the root directory of the package you want to release a new version of
(where your `setup.py` file is located):
```
$ pup
```
Then follow along with the program.

### Git tags for versioning 

We recommend using git tags as the single-source-of-truth for package
versions.

To do this, add the following lines to your `setup.py`, replacing the
`version=...` argument of the `setup()` call:
```py
setup(
    ...
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
)
```
(See also the [*setuptools_scm* documentation](https://github.com/pypa/setuptools_scm/)).

Then call `pup`, which will take care of the rest, for each new release.

Also, check-out [semantic versioning](https://semver.org).
