import logging
import time

from hystck.core.vmm import GuestListener
from hystck.core.vmm import Vmm
from hystck.utility.logger_helper import create_logger

logger = create_logger('print_documents', logging.DEBUG)
macs = []
guests = []
guest_listener = GuestListener(guests, logger)

vmm = Vmm(macs, guests, logger)
windows = vmm.create_guest(guest_name='windows_print', platform='windows')

windows.waitTillAgentIsConnected()

# Add printer
windows.shellExec('rundll32 printui.dll,PrintUIEntry /if /b IPPTool-Printer /m "Generic / Text Only" /r "http://192.168.103.123:631/ipp/print/name"')
time.sleep(3)
windows.shellExec('rundll32 printui.dll,PrintUIEntry /y /n IPPTool-Printer')
time.sleep(3)
windows.shellExec('REG ADD "HKCU\Software\Microsoft\Windows NT\CurrentVersion\Windows" /t REG_DWORD /v LegacyDefaultPrinterMode /d 1 /f')
time.sleep(5)

# Print document

#windows.runElevated('powershell -command "Get-Content -Path ./hystck-mpse_ws1920/packet_requirements.txt | Out-Printer"')
time.sleep(5)

windows.shellExec('notepad.exe /p "C:\Users\hystck\hystck\packet_requirements.txt')

# windows.remove()
