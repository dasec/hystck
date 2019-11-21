import logging
import os

from hystck.core.vmm import GuestListener
from hystck.core.vmm import Vmm
from hystck.utility.logger_helper import create_logger

# Instanciate the VM
logger = create_logger('mail_attachement', logging.DEBUG)
macsInUse = []
guests = []
guest_listener = GuestListener(guests, logger)
vmm = Vmm(macsInUse, guests, logger, 'win10')
client = vmm.create_guest(guest_name='mail_attachement_vm')

# path to the nfs mount point
nfs_path = "/data/hystck_data/"
filename = "attachement.txt"

path_to_file = os.path(nfs_path, filename)

# Wait for the VM to become ready and connect to the VMM
client.waitTillAgentIsConnected()

# Create the mailer object
mail = client.application("mailClientThunderbird", {})

# Set a password for the mail service
mail.set_session_password("hystckMailAttachementScenario")
while mail.is_busy:
    time.sleep(1)

# Load new mails
# Create a new profile to be used by thunderbird
mail.add_pop3_account("pop3.web.de", "smtp.web.de", "theo.11111@web.de", "theo.11111", "Theo Tester", "Example", 2, 3, 2, 3)
while mail.is_busy:
    time.sleep(1)
# Open thunderbird and check for mail
mail.open()
while mail.is_busy:
    time.sleep(1)
# We are done close the application
mail.close()
while mail.is_busy:
    time.sleep(1)
time.sleep(10)

# Send a new mail by invoking thunderbird with special command line options
mail.send_mail(message="testmail", subject="testmail", receiver="thomas.schaefer91@gmx.de", attachement=path_to_file)
while mail.is_busy:
    time.sleep(1)
time.sleep(10)

# We are done, shutdown and keep the VM on disk
#guest.shutdown("keep")