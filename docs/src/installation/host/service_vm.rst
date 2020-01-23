========================
Creation of the Service VM
========================

We decided to use a debian image for the service vm, but feel free to choose your favorite linux distribution. In case you choose a lnux distribution other than debian be aware that some commands of this instruction won't work on your vm. Nevertheless, the changes for the config files will stay the same for each linux distribution.

Create Service-VM:
::

	virt-install
	--name service_vm
	--ram 512
	--disk path=/var/lib/libvirt/images/service_vm.qcow2,bus=virtio,size=10,format=qcow2
	--cdrom <iso-file-of-linux-distribution>
	--network bridge=br0
	--network bridge=br1
	--graphics vnc,listen=0.0.0.0
	--noautoconsole -v

After installing the service vm, switch to your service vm and open a cli.



Setting up the mail server
========================

First we will start with the SMTP server which is primarily responsible for forwarding and storing of mails.

SMTP server:

::

$ sudo apt-get update
$ sudo apt-get install install postfix

Configuring Postfix
Edit /etc/postfix/main.cf:

::

$ myhostname = localhost
$
$ mydomain = hystck.local
$
$ myorigin = $mydomain
$
$ inet_interfaces = all
$
$ inet_protocols = all
$
$ mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain
$
$ mynetworks = 192.168.1.0/24, 127.0.0.0/8
$
$ home_mailbox = Maildir/

Restart postfix to apply the changes:
::

$ systemctl restart postfix

Now, create a test user called "hystck":
::

$ /usr/sbin/adduser hystck
$ passwd <type_a_password_of_your_choice>

Now we will install the IMAP/POP3 server:
::

$ sudo apt-get install dovecot

Add following line to the /etc/dovecot/dovecot.conf file:
::

$ protocols = imap pop3 lmtp

Add following line to the /etc/dovecot/conf.d/10-mail.conf file:
::

$ mail_location = maildir:~/Maildir

Finally, add following lines to the /etc/dovecot/conf.d/10-master.conf file (within the unix_listener auth-userdb brackets):
::

$ user = postfix
$ group = postfix

Restart dovecot to apply the changes:
::

$ systemctl restart postfix


Setting up a nfs directory
====================================
**Host side**

Installation of the nfs server:
::

$ sudo apt-get install nfs-kernel-server
$ sudo systemctl start nfs-server

Add following line to the /etc/exports/ file:
::

$ <path_to_your_nfs_directory> *(rw,sync,no_root_squash,subtree_check,nohide)

Apply changes and restart the nfs server:
::

$ sudo exportfs -a
$ sudo systemctl restart nfs-server

**Client side**

(**Windows**)

Mounting the nfs directory on a client vm (Windows)
::

$ mount -o nolock <ip_host_vm>:/<mnt_path_host_vm> z:

(Optional) Enable write permission on windows client:

- Open "regedit".
- Browse to "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\ClientForNFS\\CurrentVersion\\Default".
- Create a new "New DWORD (32-bit) Value" inside the "Default" folder named "AnonymousUid" and assign the value 0.
- Create a new "New DWORD (32-bit) Value" inside the "Default" folder named "AnonymousGid" and assign the value 0.
- Reboot the machine.

Auto startup on windows

- Press Windows+R, then type "shell:startup"
- Create a .bat file containing following commands:

::

$ @echo off
$ net use z:  \\<ip_host_vm>\<mnt_path_host_vm>

(**Linux**)

Mounting the nfs directory on a client vm (Linux)
::

$ sudo mount -t nfs4 -o proto=tcp,port=2049 <ip_host_vm>:/<mnt_path_host_vm> <mnt_path_guest_machine>




