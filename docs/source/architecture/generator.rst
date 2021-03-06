.. _gen:

****************************
Generator
****************************

The generator is an addition to make the use of hystck more user-friendly. It allows a user to hide one or multiple
needles in a haystack without needing to write a python script every time the framework is used. Additionally, after finishing
the scenario entered, the generator returns a.*pcap* file for the user to evaluate the generated traffic.

To use the generator, the user needs to configure a .*yaml* file (a template can be seen at the end of this section).
The file is structured in 4 section:

1. **collections**: This section contains a list of possible parameters such as email recipients, messages or lists of websites. The choice of what parameters are used is randomized and dependent on what seed is used - using the same seed twice should result in similar (or the same) results.

2. **applications**: This section determines which applications are used to generate traffic and execute the actions defined in the following sections.

3. **hay** and 4. **needles**: These sections define the actions that are supposed to be simulated to generate traffic. The separation between hay and needles is simply a formatting choice - it should have no bearing on what actions are allowed to be executed.


.. figure:: ../../figures/generator.PNG
    :alt: Generator workflow.

    Generator workflow.


The generator can be started with the following command:

.. code-block:: console

    $ python -m hystck.generator config.yml


What follows is depicted in the workflow diagram above. First, the virtual machine(s) is started and a connection between
host and guest is established. Then, the **config.yml** is read and the collections are loaded into the generator.
Next, the needed applications are set up and **hay** and **needles** are used to generate the actions detailed in the config file.
Before executing these actions, the parameters are chosen randomly. Once all actions have completed, the guest components
are stopped and a .*pcap* file is created on the host machine.


If you are currently not using a NFS or your NFS server is not located on your host machine, leave the fields **host_nfs_path**
and **guest_nfs_path** empty - this will allow you to use normal windows or linux paths.

============================
YAML-Template
============================

.. code-block:: xml

    name: haystack-example
    description: A example action suite to generate a haystack (traffic)
    author: MPSE Group
    seed: 1234
    collections:
        c-http-0:
            type: http
            urls: ./generator/friendly_urls.txt
        c-mail-0:
            type: mail
            recipients: ./generator/friendly_recipients.txt
            subjects: ./generator/friendly_subjects.txt
            messages: ./generator/friendly_messages.txt
        c-print-0:
            type: printer
            files: ./generator/printer_default_documents.txt
        c-smb-0:
            type: smb
            files: ./generator/general_default_attachments.txt
    settings:
        host_nfs_path: /data/hystck_data
        guest_nfs_path: Z:\\
    applications:
        mail-0:
            type: mail
            imap_hostname: imap.web.de
            smtp_hostname: smtp.web.de
            email: hystck@web.de
            password: Vo@iLmx48Qv8m%y
            username: hystck
            full_name: Heinz Hystck
            socket_type: 3
            socket_type_smtp: 2
            auth_method_smtp: 3
        mail-1:
            type: mail
            imap_hostname: 192.168.103.123
            smtp_hostname: 192.168.103.123
            email: sk@hystck.local
            password: hystck
            username: sk
            full_name: Heinz Hystck
            socket_type: 0
            socket_type_smtp: 0
            auth_method_smtp: 3
        printer-0:
            type: printer
            hostname: http://192.168.103.123:631/ipp/print/name
        smb-0:
            type: smb
            username: service
            password: hystck
            destination: \\192.168.103.123\sambashare
    hay:
        h-http-0:
            application: http
            url: https://dasec.h-da.de/
            amount: 1
        h-http-1:
            application: http
            amount: 3
            collection: c-http-0
        h-mail-0:
            application: mail-1
            recipient: sk@hystck.local
            subject: a random mail
            message: I’m sending you this mail because of X.
            attachments:
                - /data/hystck_data/blue.jpg
                - /data/hystck_data/document.pdf
            amount: 1
        h-mail-1:
            application: mail-1
            amount: 2
            recipient: sk@hystck.local
            collection: c-mail-0
    needles:
        n-printer-0:
            application: printer-0
            file: C:\Users\hystck\Documents\top_secret.txt
            amount: 2
        n-mail-0:
            application: mail-1
            recipient: sk@hystck.local
            subject: a suspicious mail
            content: I've attached said document.
            attachments:
                - /data/hystck_data/hda_master.pdf
            amount: 1
        n-smb-0:
            application: smb-0
            amount: 1
            files:
                - C:\Users\hystck\Documents\top_secret.txt
                - C:\Users\hystck\Documents\hda_master.pdf