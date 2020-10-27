import setuptools_scm
import pkg_resources


try:
    __version__ = pkg_resources.get_distribution(__name__).version
except pkg_resources.DistributionNotFound:
    # package is not installed
    __version__ = setuptools_scm.get_version(root="../..", relative_to=__file__)
