Introduction
============

Introduction to Ruruki - In-Memory Directed Property Graph
----------------------------------------------------------

What is `Ruruki <https://en.wiktionary.org/wiki/ruruki>`_? Well the technical meaning is "it is any **tool** used to extract snails from rocks".

So **ruruki** is a in-memory directed property graph database **tool** used for building complicated graphs of anything.

**Ruruki** is super useful for

* Temporary lightweight graph database. Sometimes you do not want to depend on a heavy backend that requires complicated software like Java. Or you do not have root or admin access on the server you want to run the database on. With **ruruki**, you can install it in a python virtualenv and be up and running in no time.
* Proof of concept. **Ruruki** is super great for demonstrating a proof of concept with little resources, effort, and hassle.

My idea behind using a graph database is because everything is connected in some shape or form, no matter what it is. You can apply it to things like

* Linking actors -> movies -> directors.
* Linking networks, social or computer.
* Linking people to business structures, hierarchy, or responsibilities.
* Navigation.
* Mapping which snails climb over which rocks, or tools used for extraction, and so on.
* And the list goes on, and on, and on.

You just need to change your mindset on how data is linked together, represented, and related.
Like Newton's third law "`For every action there is an equal and opposite re-action`", in terms of a graph with relationships, if one vertex/node is affected, there will be an impact on another node somewhere in the graph. For example, if the CEO is hit by a asteroid, who in the business are affected.

There are many similar projects/libraries out there that do the exact same as **ruruki**, but I decided to do my own graph library for the following reasons

* Other libraries lacked documentation.

  * `GrapheekDB <https://bitbucket.org/nidusfr/grapheekdb>`_
  * `NetworkX <https://networkx.github.io/>`_
  * `graph-tool <https://graph-tool.skewed.de/>`_
  * `python-graph <https://github.com/pmatiello/python-graph>`_

* Code was hard and complicated to read and follow.
* Others are too big and complex for the job that I needed to do.
* And lastly, I wanted to learn more about graph databases and decided writing a graph database library was the best way to wrap
  my head around it, and why not?


~~~~~~~~~~~~~~~~~~

Contributing
------------

If you would like to contribute, below are some guidelines.

* PEP8 (pylint)
* Documentation should be done on the interfaces if possible to keep it consistent.
* Unit-tests covering 100% of the code.


~~~~~~~~~~~~~~~~~~~

Versioning
----------

**Ruruki** uses the `Semantic Versioning <http://semver.org>`_ scheme.

Summary
-------

Given a version number MAJOR.MINOR.PATCH, increment the:

* MAJOR version when you make incompatible API changes,
* MINOR version when you add functionality in a backwards-compatible manner, and
* PATCH version when you make backwards-compatible bug fixes.
* Additional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR.PATCH format.


~~~~~~~~~~~~~~~~~

Functionality still being worked on
-----------------------------------

* Traversing algorithms.
* Query language.
* Extensions, for example interacting with Neo4j.
* Persistence.
* Channels for publishing and subscribing.


~~~~~~~~~~~~~~~~~

Demo
----

To see an online demo of `ruruki-eye <https://github.com/jenmud/ruruki-eye>`_ follow the following link http://www.ruruki.com.


~~~~~~~~~~~~~~~~~

Build and Testing Status
------------------------

.. image:: https://travis-ci.org/optiver/ruruki.svg?branch=master
    :target: https://travis-ci.org/optiver/ruruki

.. image:: https://coveralls.io/repos/github/optiver/ruruki/badge.svg?branch=master
    :target: https://coveralls.io/github/optiver/ruruki?branch=master

.. image:: https://codeclimate.com/github/optiver/ruruki/badges/gpa.svg
    :target: https://codeclimate.com/github/optiver/ruruki
    :alt: Code Climate

.. image:: https://img.shields.io/pypi/dm/ruruki.svg
    :target: https://pypi.python.org/pypi/ruruki

.. image:: https://img.shields.io/pypi/status/ruruki.svg
    :target: https://pypi.python.org/pypi/ruruki

.. image:: https://img.shields.io/pypi/pyversions/ruruki.svg
    :target: https://pypi.python.org/pypi/ruruki

.. image:: https://img.shields.io/pypi/dd/ruruki.svg
    :target: https://pypi.python.org/pypi/ruruki

.. image:: https://img.shields.io/pypi/dw/ruruki.svg
    :target: https://pypi.python.org/pypi/ruruki

.. image:: https://img.shields.io/pypi/dm/ruruki.svg
    :target: https://pypi.python.org/pypi/ruruki
