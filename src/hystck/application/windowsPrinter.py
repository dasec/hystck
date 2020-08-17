# Copyright (C) 2020 Marcel Meuter
# This file is part of hystck - http://hystck.fbi.h-da.de
# See the file 'docs/LICENSE' for copying permission.

try:
    import logging
    import time

    # base class VMM side
    from hystck.application.application import ApplicationVmmSide

except ImportError as ie:
    print("Import error! in windowsPrinter.py " + str(ie))
    exit(1)


class WindowsPrinterVmmSide(ApplicationVmmSide):
    """
    """

    def __init__(self, guest_obj, args):
        """Set default attribute values only.
        @param guest_obj: The guest on which this browser is running. (will be inserted from guest::application())
        @param args: containing
                hostname : Host address of the network printer.
                logger: Logger name for logging.
        """
        super(WindowsPrinterVmmSide, self).__init__(guest_obj, args)
        self.logger.info("function: WindowsPrinterVmmSide::__init__")
        self.guest = guest_obj

        self._setup_windows_network_printer(args['hostname'])

    def _setup_windows_network_printer(self, hostname):
        self.guest.shellExec(
            'rundll32 printui.dll,PrintUIEntry /if /b IPPTool-Printer /m "Generic / Text Only" /r "{}"'.format(
                hostname))
        time.sleep(3)
        self.guest.shellExec('rundll32 printui.dll,PrintUIEntry /y /n IPPTool-Printer')
        time.sleep(3)
        self.guest.shellExec(
            'REG ADD "HKCU\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Windows" /t REG_DWORD /v LegacyDefaultPrinterMode /d 1 /f')
        time.sleep(5)

    def open(self, url):
        raise NotImplementedError("This function is not implemented yet.")

    def close(self):
        raise NotImplementedError("This function is not implemented yet.")

    def print_document(self, document):
        """
        """
        self.guest.shellExec('notepad.exe /p "{}"'.format(document))
