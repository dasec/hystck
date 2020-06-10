.. _serviceinstall:

***************************
Installation of Service VM
***************************

The recommended OS for setting up the service VM is a minimal install of debian 10. Since the service VM will ideally be running constantly,
using only the most necessary of resources is preferred. Since this VM will most likely have no graphical interface, you will need to access it
using SSH.




Print Service
...................

To install the virtual printer, only a few steps are necessary. First, clone the **ippsample** tool repository:

.. code-block:: console

    $ git clone https://github.com/istopwg/ippsample.git

Navigate into the downloaded folder:

.. code-block:: console

    $ cd ippsample

Build the container:

.. code-block:: console

    $ docker build -t ippsample


You may need an updated version of docker to install the print service. Find a guide on how to install the correct docker version `here <https://docs.docker.com/engine/install/ubuntu/>`_.

Before starting the service, you need to disable encryption. To do so, a few configuration need to be changed.

.. code-block:: console

    $ docker run --name ippserver -d -rm -it -p 631:631 ippsample /bin/hash

    $ docker exec -it ippserver bash -c "mkdir -p config/print && echo Encryption Never > config/system.conf && touch config/print/name.conf"


After completing the steps above you have to simple start the service.

.. code-block:: console

    $ docker exec -it ippserver bash -c "ippserver -v -p 631 -C /config"




.. TODO install instruction service VM including DHCP server








