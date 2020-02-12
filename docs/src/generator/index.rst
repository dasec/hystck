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

Collection
^^^^^^^^^^

A collection of payloads from which the generator can choose arguments for actions
at random.

.. code-block:: yaml

    c-http-sample:
        type: http

        urls: file_each_line_one_url.txt

Application
^^^^^^^^^^^^

Corresponds to a hystck application.

.. code-block:: yaml

    n-mail-sample:
        application: mail-sample

        recipient: sample@mail.com
        subject: some subject
        content: sample content

Hay and Needles
^^^^^^^^^^^^^^^

Hay defines the inconspicuous traffic that should be generated and
needles define the suspicious traffic that should be generated.
In both sections of the configuration file actions are assigned to applications
the arguments for the actions can either be defined by hand or can be drawn from collections.

Each action is defined as a YAML object, the name being the identifier of that
payload.

.. code-block:: yaml

    n-mail-sample:
        application: mail-sample

        recipient: sample@mail.com
        subject: some subject
        content: sample content

Followed by the definition which application should handle this payload and
arguments specific to the application.

Scenarios
^^^^^^^^^

.. toctree::

    http

Sample configuration file
^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../examples/example-haystack.yaml
