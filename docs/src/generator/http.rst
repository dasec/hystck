HTTP
====

Opens given urls in the browser.

Collection
----------

.. code-block:: yaml

  c-sample-name:
    type: http
    urls: file each line one url

Application
-----------

The application for http does not need to be configured.

Action
------

.. code-block:: yaml

    a-sample-name:
        application: http
        collection: c-sample-nam
        url: https://dasec.h-da.de/
        amount: the number of urls to open

Either a hard defined url or random urls from a collection can be used.
