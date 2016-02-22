.. image:: https://travis-ci.org/optiver/ruruki.svg?branch=master
   :target: https://travis-ci.org/optiver/ruruki

.. image:: https://codeclimate.com/github/optiver/ruruki/badges/gpa.svg
   :target: https://codeclimate.com/github/optiver/ruruki
   :alt: Code Climate

=============
Documentation
=============
See ruruki `documentation here <http://ruruki.readthedocs.org/en/latest/index.html>`_.

==================
Visualization tool
==================
See rurukis' visual graph exploration tool called `Ruruki-eye <https://github.com/optiver/ruruki-eye>`_


====
Demo
====
To see an online demo of `ruruki-eye <https://github.com/optiver/ruruki-eye>`_ follow the following link http://www.ruruki.com.

What data does the demo instance have
=====================================

The demo site is a software dependency graph of the ruruki library/package.

Tips while using and navigating and exploring the data
======================================================

* Search Page

  - Is split into 4 columns, 
  
    + Label: Known labels to the graph database.
    + Property key dropdown: Every property name for that particular label.
    + filter operation type: Type of filter operation that you are performing. See `EntitySet filter <http://ruruki.readthedocs.org/en/latest/interfaces.html#entity-set>`_
    + value searching for: Value that you are searching for. Note that `*` will return all vertices for that label.
    
  - Display all vertices known to the database, click the search button with no filters.
  
* Navigating

  - Once you have clicked on a vertex from the `search page <http://ruruki.com/vertices>`_, you will see the selected vertex in the center of your page with the direct incoming and outgoing edges.
  - Double click on the bubbles to follow
  
* See the help menu on the navigation page for shortcuts.
* To show multiple levels at once, add `?levels=<number>` to the url. Eg: http://ruruki.com/vertices/0?levels=1


====
NOTE
====

  `ruruki-eye <http://www.ruruki.com>`_ is only a demo site and may feel laggy and slow. This is not a reflection on actual performance. It is recommended to `pip install ruruki-eye` locally and run it.
  


