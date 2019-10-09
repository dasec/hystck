====================
Installing the Agent
====================

Windows
-------

* Open cmd and change to *hystck\\*
* Execute::

	> python setup.py install

* Add a shortcut from  hystck\\examples\\startGuestAgent.bat to the Windows Autostart-folder


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

	$ pip install --user hystck/



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
