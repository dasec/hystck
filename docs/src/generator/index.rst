.. Usage chapter frontpage

Generator
=========

The generator takes a configuration file written in YAML and hides the defined needles in
the configured hay.

Commandline usage::

    $ python -m hystck.generator examples/example-haystack.yaml

Usage sample as a script::

    $ python examples/generate_haystack.py


Configuration file
--------

TODO

Machine
^^^^^^^

At the moment the generator can only work with one machine.

Collection
^^^^^^^^^^

A collection of payloads from which the generator can choose payloads for applications
at random.

Application
^^^^^^^^^^^

Corresponds to a hystck application.

Hay and Needles
^^^^^^^^^^^^^^^

Hay defines the inconspicuous traffic that should be generated and
needles define the suspicious traffic that should be generated.
In both sections of the configuration file payloads are assigned to applications
the payloads can either be defined by hand or can be drawn from collections.

Each payload is defined as a YAML object the name being the identifier of that
payload.

.. code-block:: yaml

    n-mail-sample:
        application: mail-sample

        recipient: sample@mail.com
        subject: some subject
        content: sample content

Followed by the definition which application should handle this payload and
arguments specific to the application.

Sample configuration file
-------------------------

.. literalinclude:: ../../../examples/example-haystack.yaml
