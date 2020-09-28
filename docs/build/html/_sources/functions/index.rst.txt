.. _funcindex:

===================
Functions of hystck
===================

Currently a selected group of applications is supported by the hystck framework. An overview can be seen in table X.


+-------------+------------------+---------+-------+
|                                |   Supported on  |
+-------------+------------------+---------+-------+
| Application | Function         | Windows | Linux |
+-------------+------------------+---------+-------+
| Firefox     |                  |         |       |
+-------------+------------------+---------+-------+
|             | open             |         |       |
+-------------+------------------+---------+-------+
|             | close            |         |       |
+-------------+------------------+---------+-------+
|             | browse_to        |         |       |
+-------------+------------------+---------+-------+
|             | facebook_login   |         |       |
+-------------+------------------+---------+-------+
| Thunderbird |                  |         |       |
+-------------+------------------+---------+-------+
|             | open             |         |       |
+-------------+------------------+---------+-------+
|             | close            |         |       |
+-------------+------------------+---------+-------+
|             | add_imap         |         |       |
+-------------+------------------+---------+-------+
|             | send_mail        |         |       |
+-------------+------------------+---------+-------+
|             | load_mailboxdata |         |       |
+-------------+------------------+---------+-------+
| VeraCrypt   |                  |         |       |
+-------------+------------------+---------+-------+
|             | open             |         |       |
+-------------+------------------+---------+-------+
|             | close            |         |       |
+-------------+------------------+---------+-------+
|             | create_container |         |       |
+-------------+------------------+---------+-------+
|             | mount_container  |         |       |
+-------------+------------------+---------+-------+
|             | copy_to_container|         |       |
+-------------+------------------+---------+-------+
|             | unmount_container|         |       |
+-------------+------------------+---------+-------+
|             | delete_container |         |       |
+-------------+------------------+---------+-------+


Firefox
=======

.. autoclass:: hystck.application.webBrowserFirefox.WebBrowserFirefoxVmmSide
    :members:


Thunderbird
===========

.. autoclass:: hystck.application.mailClientThunderbird.MailClientThunderbirdVmmSide
    :members:


VeraCrypt (command-line)
========================

.. autoclass:: hystck.application.veraCryptWrapper.VeraCryptWrapperVmmSide
    :members:

User Administration
===================

.. autoclass:: hystck.application.userManagement.UserManagementVmmSide
    :members:

Set System Time
===============

Elevated Shell Commands
=======================

(Network Share)
===============

(Network Printer Simulation)
============================

Reporter
========
The Reporter class has been added to the framework for different reasons.

.. automodule:: hystck.core.reporter
   :members:
