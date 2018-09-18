===============
What is hystck?
===============

hystck is an open source benign network traffic generator.

Some History
============

hystck started as a `master thesis`_ by Reinhard Stampp in 2013.

.. _`master thesis`: http://rstampp.net/masterthesis.pdf

Use Cases
=========

hystck is designed to create network traffic for the following applications:

    * Web Browser based
    * Mail Client related
    * Instant Messaging

New Applications can be easily added due to the modular design of hystck.

Read :doc:`../../usage/addApplication` to learn how to add a application.

Architecture
============

.. image:: architecture.png

Obtaining hystck
================

hystck can be downloaded from the `developer's website`_, where the stable and
packaged releases are distributed.

	$ wget http://141.100.55.91/download
    $ unzip hystck.zip -d $hystck
    $ cd $hystck


Otherwise it can be checked out from the `svn repository`_.

	$ svn checkout https://cased-dms.fbi.h-da.de/svn/inetsec/projects/hystck/ $hystck

We will refer $hystck as the path hystck has been downloaded or checked out to.


.. _`developer's website`: http://141.100.55.91/download
.. _`svn repository`: https://cased-dms.fbi.h-da.de/svn/inetsec/projects/hystck/