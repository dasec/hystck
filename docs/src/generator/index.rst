Generator
=========

The generator takes a configuration file written in YAML and hides the defined needles in
the configured hay.

Commandline usage::

    $ python -m hystck.generator examples/example-haystack.yaml

    $ python -m hystck.generator --help

Usage sample as a script::

    $ python examples/generate_haystack.py

Guest
^^^^^^^

At the moment the generator can only work with one guest.

Sections
^^^^^^^^^

.. toctree::

    collection
    application
    hay

Sample configuration file
^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../examples/example-haystack.yaml
