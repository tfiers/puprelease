from setuptools import find_packages, setup


GITHUB_URL = "https://github.com/tfiers/puprelease"

setup(
    name="puprelease",
    description="Publishing a new version of your Python package has never been easier",
    author="Tomas Fiers",
    author_email="tomas.fiers@gmail.com",
    url=GITHUB_URL,
    project_urls={"Source Code": GITHUB_URL},
    entry_points={"console_scripts": ["pup=puprelease.pup:pup"]},
    packages=find_packages(),
    install_requires=["click >=7,<8", "requests >=1,<3"],
    # Get package version from git tags:
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
)
