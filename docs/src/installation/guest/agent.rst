====================
Installing the Agent
====================

Windows
-------

* Checkout the `hystck-SVN-repository`_ (in the following *hystck* will be the folder containing the repository)
* Open cmd and change to *hystck\\*
* Execute::

	> python setup.py install

* Add a shortcut from  hystck\\examples\\startGuestAgent.bat to the Windows Autostart-folder

.. _hystck-SVN-repository: https://cased-dms.fbi.h-da.de/svn/inetsec/projects/hystck/

Optional: WinAdminAgent
-----------------------

WinAdminAgent is needed for manipulating the System time on Windows VMs for simulating long (in-)activity sessions.

* Open the Windows Task Scheduler
* Add a new Task for running Python with the runwinadminagent.py script
* Make sure you select run on logon and select the 'System' User as parameters
* The Admin Agent will now run in the background whenever a Desktop session begins.


Linux
-----

* Checkout and install hystck (in the following we will assume *hystck* containing the hystck repository)::

	$ svn co https://cased-dms.fbi.h-da.de/svn/inetsec/projects/hystck/ --username $YOUR_USERNAME_HERE$ hystck/
	$ pip install --user hystck/

.. No longer needed due to new code with os-awareness
.. #. Remove Windows Dependecies
.. 	::
.. 
.. 		$ cd ~/.local/lib/python2.7/site-packages/hystck # install location from python setup.py install
.. 
.. 	a. agent.py
.. 		::
.. 
.. 			$ nano src/core/agent.py
.. 
.. 		Add comments to the following lines from the top of the file:
.. 
.. 		.. code:: python
.. 
.. 			from hystck.utility.SendKeys import SendKeys
.. 			....
.. 			from hystck.utility.window import get_win_id_from_window
.. 			from hystck.utility.window import raise_window_by_name
.. 			from hystck.utility.window import raise_window_by_win_id
.. 			from hystck.inputDevice.mouse import mouse_click
.. 			from hystck.inputDevice.mouse import relative_mouse_click
.. 
.. 		and from Agent.__init__() comment out:
.. 
.. 		.. code:: python
.. 
.. 		    self.inputDeviceManager = InputDeviceManagement(self, logger)
.. 
.. 	b. window.py
.. 		::
.. 
.. 	    	$ nano src/utility/window.py
.. 
.. 		#Replace::
.. 
.. 			raise Exception("Error window.py " + str(e))
.. 
.. 		from the top of the file with:
.. 
.. 		.. code:: python
.. 
.. 			pass
.. 
.. 
.. 	c. window.py
.. 		::
.. 
.. 			$ nano src/inputDevice/window.py
.. 
.. 		Comment out:
.. 
.. 		.. code:: python
.. 
.. 			from hystck.inputDevice.keyboard import KeyboardManagement
.. 			from hystck.inputDevice.mouse import MouseManagement


* Configure Ubuntu to start guestAgent.py on every system startup:


	Create startup script (Removed multiline character > from shell-output for easier copy-and-paste). The sleep-command tries to cover the time the DHCP needs set the IP-addresses
		::

			$ cat > ~/.config/autostart/bash.desktop <<EOL
			[Desktop Entry]
			Type=Application
			Exec=/usr/bin/gnome-terminal -e "bash -c 'sleep 45 && python /home/hystck/hystck/examples/guestAgent.py; bash'"
			Hidden=false
			NoDisplay=false
			X-GNOME-Autostart-enabled=true
			Name=StartAgent
			EOL
