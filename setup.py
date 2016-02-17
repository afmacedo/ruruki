#!/usr/bin/env python
import os.path
from setuptools import setup, find_packages


def auto_version_setup(**kwargs):
    pkg_name = kwargs["packages"][0]

    # Populate the "version" argument from the "VERSION" file.
    pkg_path = os.path.join(os.path.dirname(__file__), pkg_name)
    with open(os.path.join(pkg_path, "VERSION"), "r") as handle:
        pkg_version = handle.read().strip()
    kwargs["version"] = pkg_version

    # Make sure the "VERSION" file is included when we build the package.
    package_data = kwargs.setdefault("package_data", {})
    this_pkg_data = package_data.setdefault(pkg_name, [])
    if "VERSION" not in this_pkg_data:
        this_pkg_data.append("VERSION")

    setup(**kwargs)


auto_version_setup(
    name="ruruki",
    author="Jenda Mudron",
    author_email="Jenda.Mudron@optiver.com.au",
    maintainer="Jenda Mudron",
    maintainer_email="Jenda.Mudron@optiver.com.au",
    url="https://github.com/optiver/ruruki",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2 :: Only",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Software Development :: Libraries",
    ],
    keywords="graph db momory database in-memory snail extraction tool",
    description="Ruruki is a in-memory graph database.",
    long_description=open("README.rst").read(),
    packages=find_packages(),
    package_data={
        "ruruki": [
            "VERSION",
        ],
    },
    install_requires=[],
    entry_points = {
        "ruruki.graphs": [
            "graph = ruruki.graphs:Graph",
        ],
    },
)
