from setuptools import find_packages, setup


GITHUB_URL = "https://github.com/tfiers/puprelease"

with open("ReadMe.md", mode="r") as f:
    readme = f.read()

setup(
    name="puprelease",
    description="Publishing a new version of your Python package has never been easier",
    author="Tomas Fiers",
    author_email="tomas.fiers@gmail.com",
    long_description=readme,
    long_description_content_type="text/markdown",
    url=GITHUB_URL,
    project_urls={"Source Code": GITHUB_URL},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["pup=puprelease.pup:pup"]},
    packages=find_packages(),
    install_requires=["click ~=7.0", "requests ~=2.0", "twine", "setuptools_scm"],
    # Get package version from git tags
    setup_requires=["setuptools_scm"],
    use_scm_version={
        "version_scheme": "post-release",
        "local_scheme": "dirty-tag",
    },
)
