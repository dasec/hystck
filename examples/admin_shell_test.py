import time
import logging
import subprocess
from hystck.core.vmm import Vmm
from hystck.utility.logger_helper import create_logger
from hystck.core.vmm import GuestListener

# Instanciate VMM and a VM
logger = create_logger('hystckManager', logging.DEBUG)
macsInUse = []
guests = []
guestListener = GuestListener(guests, logger)
virtual_machine_monitor1 = Vmm(macsInUse, guests, logger)
guest = virtual_machine_monitor1.create_guest(guest_name="adminshelltest", platform="windows")

# Wait for the VM to connect to the VMM
guest.waitTillAgentIsConnected()

guest.setOSTime("2019-01-01 12:00:00")

guest.runElevated('net user John fadf24as /ADD')

time.sleep(10)

#guest.shutdown("keep")