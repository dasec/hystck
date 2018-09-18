============
Requirements
============

Before proceeding on configuring hystck, you'll need to install some required
software and libraries.

Installing Python libraries
===========================

hystck host components are completely written in Python, therefore make sure to
have an appropriate version installed. For the current release **Python 2.7** is preferred.

Install Python on Ubuntu::

    $ sudo apt-get install python

Additionally you need the hypervisor.

If want to use KVM it's packaged too and you can install it with the following command::

    $ sudo apt-get install qemu-kvm libvirt-bin bridge-utils virt-manager

.. CloneManager is no longer used, ergo comment it out
.. Replace CloneManager::
..
..    $ mv $hystck/templates/CloneManager.py /usr/lib/python2.7/dist-packages/virtinst/CloneManager.py

Virt-Install modules seem no longer to be in python default module path in some major distributions.
If hystck tells you that dummy modules were imported you may be affected or missed to install virt-install or it's containing package.

You can fix this issue by adding the path by hand for example via an alias::

    $ alias python="PYTHONPATH=/usr/share/virt-manager/ python"

The following module install steps are also needed:

Install psutil::

    $ pip install psutil

Install marionette_driver::
    
    $ pip install -U marionette_driver

Install mozprofile::

    $ pip install -U mozprofile

Install mozrunner::

    $ pip install -U mozrunner


The Bot-Framework needs the following additional Python modules:

Install module enum34::

	$ pip install enum34

Install module protobuf-2.5.0::

	$ pip install protobuf==2.5.0

    
Installing Tcpdump
==================

In order to dump the network activity performed by the application during
execution, you'll need a network sniffer properly configured to capture
the traffic and dump it to a file.

By default hystck adopts `tcpdump`_, the prominent open source solution.

Install it on Ubuntu::

    $ sudo apt-get install tcpdump

Tcpdump requires root privileges, but since you don't want hystck to run as root
you'll have to set specific Linux capabilities to the binary::

    $ sudo setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump

You can verify the results of last command with::

    $ getcap /usr/sbin/tcpdump
    /usr/sbin/tcpdump = cap_net_admin,cap_net_raw+eip

If you don't have `setcap` installed you can get it with::

    $ sudo apt-get install libcap2-bin

Or otherwise (**not recommended**) do::

    $ sudo chmod +s /usr/sbin/tcpdump

.. _tcpdump: http://www.tcpdump.org


Installing NFS-Server
=====================
Hystck does not depend on specific implementation of a shared filesystem, but it will assume all template image files being available on all server, which can be easily achived by a shared filesystem.
::

    $ sudo apt-get install nfs-kernel-server
    $ cat /etc/exports
    ...
    /export       141.100.55.0/24(rw,sync,no_root_squash,subtree_check)
    /export/hystck 141.100.55.0/24(rw,sync,no_root_squash,subtree_check,nohide)
    ...

    $ sudo mount --bind ~/hystck_data /export/hystck

Where ~/hystck_data is the original storage pool for image templates.


On every other system, where you would like to mount the NFS, you have to:
::

    $ sudo mount -t nfs4 -o proto=tcp,port=2049 141.100.55.74:/ /mnt/hystck

Where 141.100.55.74 has to be replaced the by NFS-Server-IP. See https://help.ubuntu.com/community/SettingUpNFSHowTo for detailed instructions.


Installing Spice (optional)
===========================

This step is not required, but will make further steps easier, because Spice enables Copy-and-Paste between Host and Guest::

	$ sudo apt-get install spice-client
	$ sudo apt-get install spice-client-gtk
	$ sudo apt-get install python-spice-client-gtk
