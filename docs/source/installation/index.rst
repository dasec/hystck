.. _installindex:

**********************
Installation of hystck
**********************

Hystck is a framework that consists of two distinct parts as we described in
:ref:`Architecture of hystck <architecture_index>`. For that reason
it is mandatory to install hystck on both, the host and the guest system. In the next sections we will show how that
installation can be done.


Installation Host (physical machine)
####################################

Here we will describe how to install the host part of hystck on a physical machine.

For this **Ubuntu 19.10** is the recommended OS. Other Ubuntu distributions will work as well, but the automatic setup
script might need some alterations depending on your distribution.

Instructions can be found in :ref:`hostinstall`.

Installation Guest (virtual machine)
####################################

Here we will describe how to install the guest part of hystck on a virtual machine as well as creating said virtual
machine with everything needed for hystck to operate correctly.

An in-depth installation manual can be found here: :ref:`guestinstall`.

Windows
*******
Instructions will follow here shortly.

Setup the virtual machine and install Windows like you normally would (or download our template at: ). After that
follow the simple steps in the list below.

#. Download hystck source code inside VM
#. Download additional MSI installers for C++ and Python
#. extract hystck source code to a folder on the Desktop of your virtual machine
#. open the folder *hystck/install*
#. start windows_setup.bat

Linux
*****
Instructions will follow here shortly.

Setup the virtual machine and install Ubuntu like you normally would (or download our template at: ). After that
follow the simple steps in the list below.

#. Download hystck source code inside VM
#. extract hystck source code to a folder on the Desktop of your virtual machine
#. open the folder *hystck/install*
#. start linux_setup.sh



Installation Service VM
#########################


Here we will describe how to install the Service VM containing third party services that enhance hystck's capabilities
such as a DHCP server as well as services needed for specific scenarios.

Instructions will follow here shortly.