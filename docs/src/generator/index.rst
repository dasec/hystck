.. Usage chapter frontpage

Generator
=========

The generator takes a configuration file written in YAML and hides the defined needles in
the configured hay.

Commandline usage::

    $ python -m hystck.generator examples/example-haystack.yaml

Usage sample as a script::

    $ python examples/generate_haystack.py

Sample configuration file:

.. literalinclude:: ../../../examples/example-haystack.yaml

Concepts
--------

TODO

Machine
^^^^^^^

TODO

Collection
^^^^^^^^^^

TODO

Application
^^^^^^^^^^^

Corresponds to a hystck application.

Hay
^^^^^^^^^^^

The inconspicuous traffic that should be generated.

Needle
^^^^^^^^^^^

The suspicious traffic that should be generated.
