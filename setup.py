# Copyright 2023 Alexander L. Hayes

"""
Setup file for babybear
"""

# TODO(hayesall): Don't hard-code the __version__ number.
__version__ = "0.1.0"


from setuptools import setup
from setuptools import find_packages
from codecs import open
from os import path


_here = path.abspath(path.dirname(__file__))
with open(path.join(_here, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()


setup(
    name="babybear",
    packages=find_packages(exclude=["tests"]),
    package_dir={"babybear": "babybear"},
    author="Alexander L. Hayes (hayesall)",
    author_email="alexander@batflyer.net",
    version=__version__,
    description="A microscopic data manipulation based on pandas, but tiny.",
    long_description=LONG_DESCRIPTION,
    url="https://hayesall.com",
    download_url="https://github.com/hayesall/babybear/",
    license="MIT License or Apache License, version 2.0",
    zip_safe=True,
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: Apache Software License",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="dataframe data-science teaching data-analysis teaching-tool",
    install_requires=[],
    extras_require={
        "tests": ["coverage", "pytest"],
    },
)
