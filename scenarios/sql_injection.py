import logging

from hystck.core.vmm import GuestListener
from hystck.core.vmm import Vmm
from hystck.utility.logger_helper import create_logger

logger = create_logger('sql_injection', logging.DEBUG)
macs = []
guests = []
guest_listener = GuestListener(guests, logger)

vmm = Vmm(macs, guests, logger)
server = vmm.create_guest(guest_name='sql_injection_server', platform='linux')
client = vmm.create_guest(guest_name='sql_injection_client', platform='linux')
server.waitTillAgentIsConnected()
client.waitTillAgentIsConnected()

# install web server on server
# install curl on client if necessary

# serve simple login form
# perform sql injection on form

server.remove()
client.remove()
