import logging
import os
import time

from hystck.core.vmm import GuestListener
from hystck.core.vmm import Vmm
from hystck.utility.logger_helper import create_logger

# Instanciate the VM
logger = create_logger('mail_attachement', logging.DEBUG)
macsInUse = []
guests = []
guest_listener = GuestListener(guests, logger)
vmm = Vmm(macsInUse, guests, logger)

# add a check to see if the vm already exists
client = vmm.create_guest(guest_name='mail_attachement_vm')

# path to the nfs mount point
nfs_path = "/data/hystck_data/"
filename = "attachement.txt"
path = "C:\Users\hystck\Documents\document.txt"

path_to_file = os.path.normpath(path)

# Wait for the VM to become ready and connect to the VMM
client.waitTillAgentIsConnected()

# Create the mailer object
mail = client.application("mailClientThunderbird", {})

# Set a password for the mail service
mail.set_session_password("Vo@iLmx48Qv8m%y")
while mail.is_busy:
    time.sleep(1)

# Load new mails
# Create a new profile to be used by thunderbird
mail.add_imap_account("imap.web.de", "smtp.web.de", "hystck@web.de", "hystck@web.de", "hystck", "web smtp server")
while mail.is_busy:
    time.sleep(1)

time.sleep(20)

# Open thunderbird and check for mail
mail.open()
while mail.is_busy:
    time.sleep(1)
# We are done close the application
mail.close()
while mail.is_busy:
    time.sleep(1)
time.sleep(6)

# Send a new mail by invoking thunderbird with special command line options
mail.send_mail(message="testmail", subject="testmail", receiver="martin-thissen97@web.de")
while mail.is_busy:
    time.sleep(1)
time.sleep(10)

# We are done, shutdown and keep the VM on disk
# guest.shutdown("keep")
