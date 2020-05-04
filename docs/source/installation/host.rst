.. _hostinstall:

**********************
Host Installation
**********************

The installation of the host component of hystck can be done automatically using **pre_setup.py** and the corresponding
**config.json** located in the install_tools folder. Please check :ref:`config` before you start any of the installation
scripts and make adjustments where necessary. If you are using a different Ubuntu distribution than recommended in
:ref:`installindex`, you might need to tweak either file or run a completely manual installation of the host component.

.. Regardless of what method you choose, you first need to install python.

Installation Host -- scripted
####################################

The partially automated installation requires just a few steps to set up the host components of hystck.

First, make sure the name of the user and your chosen paths for the virtual machine data, the location of your cloned hystck
repository and the path to your tcpdump binary you want to install hystck on is correctly configured in **config.json** (:ref.
This is important, since the setup script later adds this user to the libvirtd-group,
which is required to create clones of the virtual guest machines.

.. TODO BACKING FOLDER MANUELL/NICHT ALS SUDO??? DANN CHOWN AUF KREEIRTE IMAGES(IN GUEST SEITE UNTERBRINGEN
- LIBVIRT QEMU ODER CURRENT USER? LIBVIRT QEMU HAT FUNKTIONIERT, JETZT CURRENT USER) EVTL ÜBER POOL XML?
-add changes to /etc/qemu.conf (uncomment root user & group?) -> separate trouble shooting section?

.. TODO Backing als xml oder als mkdir und dann chown -r beide varianten in presetup, bei xml varianten müssen cmö von hystck
pool und backing pool um usernamen ergänzt werden

.. TODO image chown OR TEST VIA QEMU.CONF dynamic ownership usw

.. TODO hystck-pool.xml UPLOAD/ÜBERTRAGEN VON UBUNTU LAPTOP UND IN PRESETUP EINBINDEN UND HIER NÖTIGE ANPASSUNGEN ERWÄHNEN/BZW AUTOMATISIEREN ÜBER CONFIG UND id -u user

.. TODO => chown jetzt in presetup; need one more chown AFTER template creation (virt install scripts via python?)

.. TODO adduser to sudo; change paths and username in config.json; make sure to download & install with correct user
.. TODO check if user is correct through linux installation -> error if not correct
.. TODO Clone into correct users' paths
.. TODO second setup.py for automated install ../src/hystck path instead of src/hystck change call in presetup, ../utility in setup py or src hystck utility
.. TODO skip pywin32 in linux
.. TODO mkdir backing folder; change section in installation#
.. TODO backing and pool path in constants and config need to be adjusted to same -> manual sudo mkdir backing
.. TODO  ?? qemu config add user etc libvirt qemuconf dynamic ownership 0 ??
.. TODO give access to new user to use GUI echo $DISPLAY is blank - error with installation?
.. TODO hystck pool user change
.. TODO libvirt user privileges, login needed after reboot??? -> libvirt and libvirtd privileges for new user
.. TODO logout/exit restart terminal sessions instead of reboot

.. TODO: gui privileges: xauth, reboot???, xhost +, echo $DISPLAY, su - user, export DISPLAY=[result of echo]
.. TODO: xauth xhost variant only temp: edit .bashrc -> add export DISPLAY=:0 or equivalent (echo $DISPLAY) -> add to presetup
    -> add to config.json WHICH display :0 default -> still needs xauth & xhost + beforehand FIND PERMANENT SOLUTION
    -> xauth, exit, xhost +, su - user

.. TODO: terminal restart statt reboot

.. TODO: skip pywin32 on platform linux

.. TODO: If... Else pre setup (if installation aborts -> pre setup aborted etc)

.. TODO: LIBVIRT FOLDER RIGHTS CANT CREATE BACKING IMAGES

A new user can be added with the following command:

.. code-block:: console

    $ sudo adduser hystck

If you want to install hystck on a new user, please create that user **before** running any part of the installation process.
Additionally, it is imperative to give the new user root permissions as the installation script has to be called with sudo.

.. code-block:: console

    $ sudo usermod -a -G sudo hystck


In these two examples replace **hystck** with a username of your choice. Make sure it matches the username in **config.json**.


To run the following commands, you will need to download hystck now.
Hystck can be found here: `Github link <https://github.com/dasec/hystck>`_.
Clone or download the repository and navigate into **/install_tools**.

In this folder, you will find a shell script called **linux_installation.sh**. To install the further parts of hystck's
host component, run the script with root privileges and choose **h** when the console prompts you to make a choice. The
script will then install all necessary packages including the appropriate Python version.


.. code-block:: console

    $ sudo ./linux_installation.sh
    Please choose if this installation is host (h) or guest (g) side installation:
    Selection: h
    ...


This then runs the **pre_setup.py** with the  **host** parameter to start installing all
necessary packages and python modules. You can also start this script by hand if you choose to do so, although it would
require a manual installation of Python beforehand.

.. TODO Part of linux installation script

.. code-block:: console

    $ sudo python pre_setup.py host

After installing all packages and python modules, the script sets up permissions for the
appropriate user to create clones of the virtual guest environments by creating the libvirtd group and adding
the user mentioned in **config.json** to that group. Additionally, rights for the user to run tcpdump are given.
**pre_setup.py** then creates both the virtual machines pool and the network bridges. If you need to adjust any of the
default paths for your pools or the location of tcpdump, you can do so in **config.json** (see: :ref:`config`)
All of these steps will be described further in the next section **Installation Host -- manual**.

Important note: It is possible, that the **backing** folder inside the created pool location is missing, which
means you have to add it manually before running any **hystck** commands. If your pool is located in **/data**,
simply add a folder **/data/[pool-name]/backing**. You can also remove **backing** part of the path in
**/src/hystck/utility/constants.py**

.. TODO: code snippet?


Lastly, hystck needs to be installed. Navigate into the folder and then run:

.. code-block:: console

    $ python setup.py install --user


Installation Host -- manual
####################################

In case there are any issues with the partially automatic installation, you are using a different Ubuntu distribution
or simply want to adapt the installation process to a different OS, this section will guide you through the entire
host-side installation process.

By default, only python 3 is installed on the recommended Ubuntu distribution, but hystck is
currently still running on python 2. The following command should install python 2.7.

.. code-block:: console

    $ sudo apt install python


You can check your python version:

.. code-block:: console

    $ python -V


If somehow your default python is still python 3, you can change this using the following guidelines:

.. TODO update-alternatives guide


First, you will also want to create the user named **hystck**. This default user is chosen by us to make the following
steps (e.g. rights management) easier. You can use your default or any other user, just make sure to adapt the further
steps mentioning the hystck user to your chosen username.

.. code-block:: console

    $ sudo adduser hystck --disabled-login --no-create-home

Next, you need to install the required packages.

.. code-block:: console

    $ sudo apt install python-pip
    $ sudo apt install python-libvirt
    $ sudo apt install qemu-kvm
    $ sudo apt install libvirt-bin
    $ sudo apt install libvirt-dev
    $ sudo apt install virt-manager
    $ sudo apt install libcap2-bin
    $ sudo apt install tcpdump

The required packages can also be found in **/install_tools/packet_requirements.txt**.

.. TODO describe what packages do (same for pip)

In a similar manner, all necessary python packages need to be installed.

.. code-block:: console

    $ pip install -U pywinauto
    $ pip install -U pywin32
    $ pip install -U setuptools
    $ pip install -U selenium
    $ pip install -U marionette_driver
    $ pip install -U netifaces
    $ pip install -U psutil
    $ pip install -U netaddr
    $ pip install -U enum34
    $ pip install -U protobuf==2.5.0

These packages can also be located under **/install_tools/PIP_requirements.txt**.

The default network sniffer chosen by hystck ist tcpdump. Usually, tcpdump requires root privileges to function
properly, but since it should not be a requirement to run hystck with root privileges, a simple modification to tcpdump
needs to be made.

.. code-block:: console

    $ sudo setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump

Naturally, you will need to verify if tcpdump ist located in the folder used by this command an potentially adjust the
path. You can check if the change was successful by entering the following command:

.. code-block:: console

    $ getcap /usr/sbin/tcpdump
    /usr/sbin/tcpdump = cap_net_admin,cap_net_raw+eip     "This is the output you should get"

In case this solution does not work for you, you can simply give tcpdump the necessary privileges:

.. code-block:: console

    $ sudo chmod +s /usr/sbin/tcpdump

Another privilege issue concerns libvirtd and the created hystck user. Only root and members of the **libvirtd** group
are able to fully access and modify the virtual machine images. To remedy this situation, we first usually have to create
the libvirtd group. After creating the group, we can add the hystck user to it.

.. code-block:: console

    $ sudo groupadd libvirtd
    $ sudo usermod -a -G libvirtd hystck

Following the installation of all necessary packages, we need to create the virtual machine pools. This is were our
guest components original and instanced images are stored. To do so, run the following four commands:

.. code-block:: console

    $ virsh pool-define-as hystck-pool dir - - - - "data/hystck-pool"
    $ virsh pool-build hystck-pool
    $ virsh pool-start hystck-pool
    $ virsh pool-autostart hystck-pool

The path **/data/hystck-pool** has to be created manually beforehand. After running the commands above, you might
want to add a directory named **backing** into **/data/hystck-pool** - this is where the clones of our guest images
are going to be stored. You can check your pools with the following commands:
.. TODO: check if true (has to be created manually)

.. code-block:: console

    $ virsh pool-list --all
    $ virsh pool-info hystck-pool


To run the following commands, you will need to download hystck now.
Hystck can be found here: `Github link <https://github.com/dasec/hystck>`_.
Clone or download the repository and navigate into **/install_tools**. Here, you will find **private.xml** and
**public.xml**. These two files will help you to set up the network connections needed to communicate between the
guest and the host without tainting the actual internet traffic hystck is creating. The following set of commands
will use the XML templates provided.

.. code-block:: console

    $ virsh net-define public.xml
    $ virsh net-define private.xml

    $ virsh net-start public
    $ virsh net-start private

    $ virsh net-autostart public
    $ virsh net-autostart private


Similarly to the pools, you can check your created networks:

.. code-block:: console

    $ virsh net-list
    $ virsh net-dumpxml [name]
    $ virsh net-info [name]


Lastly, hystck needs to be installed. Navigate into the folder and then run:

.. code-block:: console

    $ python setup.py install --user





Troubleshooting
###################################

.. code-block:: console

    $ sudo apt install ebtables  "If there are KVM or firewall errors"
    $ sudo apt install dnsmasq  "If there are general Network issues"
    $ sudo apt install qemu-utils "If KVM gives warnings about performance"
    $ sudo chmod 755 [path/to/**backing**} "If KVM has issues with creating differential images"
