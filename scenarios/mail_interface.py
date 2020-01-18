import logging
import os
import time
import shutil

from hystck.core.vmm import GuestListener
from hystck.core.vmm import Vmm
from hystck.utility.logger_helper import create_logger
from enum import Enum

# Instanciate the VM
logger = create_logger('mail_attachement', logging.DEBUG)
macsInUse = []
guests = []
guest_listener = GuestListener(guests, logger)
vmm = Vmm(macsInUse, guests, logger)

# add a check to see if the vm already exists
client = vmm.create_guest(guest_name='mail_attachement_vm')

# path to the nfs mount point
_guest_vm_nfs_path = 'Z:\\'
nfs_path = "/data/hystck_data/"
filename = "attachement.txt"
path = 'C:\Users\hystck\Documents\document.txt'
path_pdf = 'C:\Users\hystck\Documents\hda_master.pdf'

path_to_file = os.path.normpath(path)
path_to_pdf = os.path.normpath(path_pdf)

# Wait for the VM to become ready and connect to the VMM
client.waitTillAgentIsConnected()

# Create the mailer object
thunderbird_guest_vm = client.application("mailClientThunderbird", {})

class Color(Enum):
    red = 1


class MailAccount:
    # TODO ENUM Socket types
    def __init__(self, imap_server, smtp_server, email_address, password, user_name, socket_type, auth_method, socket_type_smtp, auth_method_smtp):
        self.imap_server = imap_server
        self.smtp_server = smtp_server
        self.email_address = email_address
        self.password = password
        self.user_name = user_name
        self.socket_type = socket_type
        self.auth_method = auth_method
        self.socket_type_smtp = socket_type_smtp
        self.auth_method_smtp = auth_method_smtp


class Mail:
    def __init__(self, recipient, subject, body, attachment_path_list=None):
        self.recipient = recipient
        self.subject = subject
        self.body = body
        self.attachment_path_list = attachment_path_list


class IllegalArgumentError(ValueError):
    pass


def send_mail(guest_vm, mail_account, mail):
    if not isinstance(mail, Mail):
        raise IllegalArgumentError("Wrong object type. Please pass for the argument mail an instance of type Mail.")

    if not isinstance(mail_account, MailAccount):
        raise IllegalArgumentError("Wrong object type. Please pass for the argument mail_account an instance of type MailAccount.")

    # TODO Prove if file is in nfs directory
    if mail.attachment_path_list is not None:
        mail.attachment_path_list = generate_path_list_for_guest_vm(mail.attachment_path_list, _guest_vm_nfs_path, nfs_path)


    # Set a password for the mail service
    guest_vm.set_session_password(mail_account.password)

    while guest_vm.is_busy:
        time.sleep(1)

    # Load new mails
    # Create a new profile to be used by thunderbird
    guest_vm.add_imap_account(mail_account.imap_server, mail_account.smtp_server, mail_account.email_address, mail_account.user_name, mail_account.socket_type, mail_account.socket_type_smtp, mail_account.auth_method_smtp)

    while guest_vm.is_busy:
        time.sleep(1)

    time.sleep(20)

    # Open thunderbird and check for mail
    guest_vm.open()

    while guest_vm.is_busy:
        time.sleep(1)
    # We are done close the application
    guest_vm.close()

    while guest_vm.is_busy:
        time.sleep(1)
    time.sleep(6)

    # Send a new mail by invoking thunderbird with special command line options
    guest_vm.send_mail(message=mail.body, subject=mail.subject, receiver=mail.recipient, attachment_path_list=mail.attachment_path_list)

    while guest_vm.is_busy:
        time.sleep(1)
    time.sleep(30)


def generate_path_list_for_guest_vm(attachment_path_list, guest_vm_nfs_path, host_vm_nfs_path):
    validated_file_list = []
    for file_path in attachment_path_list:
        if os.path.isfile(path):
            if os.path.dirname(path) == host_vm_nfs_path:
                guest_vm_file_path = generate_nfs_path_for_file_on_guest_vm(file_path, guest_vm_nfs_path)
                validated_file_list.append(guest_vm_file_path)
            else:
                print "ERROR: " + file_path + "is not located within the host nfs directory: " + host_vm_nfs_path
        else:
            print "ERROR: " + file_path + " is not a valid file path."
    return validated_file_list


def generate_nfs_path_for_file_on_guest_vm(file_path, guest_vm_nfs_path):
    return os.path.normpath(guest_vm_nfs_path + os.path.basename(file_path))


web_mail_account = MailAccount("imap.web.de", "smtp.web.de", "hystck@web.de", "password", "hystck", 3, 3, 2, 3)
local_mail_account = MailAccount("192.168.103.123", "192.168.103.123", "sk@hystck.local", "password", "sk", 0, 3, 0, 3)


first_mail = Mail(recipient="martin-thissen97@web.de", subject="testmail", body="testmail", attachment_path_list=[path_to_file, path_to_pdf])
second_mail = Mail(recipient="martin-thissen97@web.de", subject="testmail", body="testmail")
third_mail = Mail(recipient="sk@hystck.local", subject="testmail", body="testmail", attachment_path_list=[path_to_file, path_to_pdf])

# send mails
send_mail(guest_vm=thunderbird_guest_vm, mail_account=web_mail_account, mail=first_mail)
send_mail(guest_vm=thunderbird_guest_vm, mail_account=web_mail_account, mail=second_mail)
send_mail(guest_vm=thunderbird_guest_vm, mail_account=local_mail_account, mail=third_mail)