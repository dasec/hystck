import time
import logging
import os
import config as cfg

from hystck.core.vmm import Vmm
from hystck.utility.logger_helper import create_logger
from hystck.core.vmm import GuestListener

imagename = cfg.imagename
author = cfg.author
hostplatform = cfg.hostplatform

sourcePath = "C:\Users\hystck\Desktop\TestFile.txt"
targetPath = "Z:\TestFile.txt"

# Instanciate VMM and a VM
logger = create_logger('hystckManager', logging.DEBUG)
macsInUse = []
guests = []


# TODO: Create VM only if non existent
guestListener = GuestListener(guests, logger)
virtual_machine_monitor1 = Vmm(macsInUse, guests, logger)
guest = virtual_machine_monitor1.create_guest(guest_name=imagename, platform=hostplatform)
# TODO: Start smb-server
# smbServer = virtual_machine_monitor1.create_guest(guest_name=cfg.smbname, platform=cfg.smbplatform)

# Wait for the VM to connect to the VMM
guest.waitTillAgentIsConnected()
# smbServer.waitTillAgentIsConnected()

# TODO: reconnect SMB share in windows
time.sleep(120)
# copy files to smb Share
guest.guestCopy(os.path.normpath(sourcePath), os.path.normpath(targetPath))


# Cleanup
#guest.cleanUp("")
#guest.shutdown('keep')

