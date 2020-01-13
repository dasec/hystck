import logging

from hystck.core.vmm import GuestListener
from hystck.core.vmm import Vmm
from hystck.utility.logger_helper import create_logger

logger = create_logger('print_documents', logging.DEBUG)
macs = []
guests = []
guest_listener = GuestListener(guests, logger)

vmm = Vmm(macs, guests, logger)
# server = vmm.create_guest(guest_name='print_documents_server', platform='linux')
# client = vmm.create_guest(guest_name='print_documents_client', platform='linux')
# server.waitTillAgentIsConnected()
# client.waitTillAgentIsConnected()

# # print a document
# server.remove()
# client.remove()
