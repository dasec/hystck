# Copyright (C) 2018 Sascha Kopp
# This file is part of hystck - http://hystck.fbi.h-da.de
# See the file 'docs/LICENSE' for copying permission.
# This version of the mail client plugin uses the native mozilla python modules for manipulating the configuration to reduce code bloat
# See hystck.utility.tbstuff.py for profile manipulation functions

# IMPORTANT!!!
# Bugs and issues:
# For some reason creating the profile may fail, check the error variable for this application after calling the add profile methods.
# Last test worked, just make sure profiles.ini can be accessed.
# Send_mail only works if Thunderbird is closed, pywinauto seems to fail in connecting to the window if Thunderbird is already opened
# Linux side has not been updated and may fail for receiving an sending mail
# For some reason adding an imap account makes Thunderbird fail to provide the correct choices while manually switching authentification methods, it should not matter
# For another unknown reason Thunderbird will ignore the common entries for the local folders and add an additional entry section for it, does not seem to affect anything

try:
    import logging
    import os
    import shutil  # to delete folders with content
   # import sys
    import platform
    import threading
    import subprocess
    import time
    import inspect  # for listing all method of a class
    import base64

    # base class VMM side
    from hystck.application.application import ApplicationVmmSide
    from hystck.application.application import ApplicationVmmSideCommands

    # base class guest side
    from hystck.application.application import ApplicationGuestSide
    from hystck.application.application import ApplicationGuestSideCommands
    from hystck.utility.line import lineno
    from hystck.utility.io import parse_attachment_string
    from hystck.utility.io import escape_password_string

    if platform.system() == "Windows":
        import pywinauto
        from hystck.utility.SendKeys import SendKeys

    import hystck.utility.picklehelper as ph
    import hystck.utility.tbstuff as tbs
    from smbclient import (
    shutil
)

except ImportError as ie:
    print("Import error! in fileTransfer.py " + str(ie))
    exit(1)


###############################################################################
# Host side implementation
###############################################################################
class FileTransferVmmSide(ApplicationVmmSide):
    """
    This class is a remote control on the host-side to control multiple File Sharing operations
    running on a guest.
    """

    def __init__(self, guest_obj, args):
        """Set default attribute values only.
        @param guest_obj: The guest on which this application is running. (will be inserted from guest::application())
        @param args: containing
                 logger: Logger name for logging.
        """
        try:
            super(FileTransferVmmSide, self).__init__(guest_obj, args)
            self.logger.info("function: fileTransferVmmSide::__init__")
            self.window_id = None
            self.window_id = self.guest_obj.current_window_id
            self.guest_obj.current_window_id += 1

        except Exception as e:
            raise Exception(lineno() + " Error: fileTransferVmmSide::__init__ "
                            + self.guest_obj.guestname + " " + str(e))


    def smbCopy(self, guest_source_path, smb_target_path, user, passw):
        """ Copies file from guest to smb share.
                :param guest_source_path: source path on guest
                :param smb_target_path: target path on smb
                :param user: smb user
                :param passw: pass
        """
        try:
            #msg = base64.b64encode(guest_source_path) + " " + base64.b64encode(smb_target_path) + " " + base64.b64encode(user) + " " + base64.b64encode(passw)
            msg = {"guest_source_path": guest_source_path,
                  "smb_target_path": smb_target_path,
                  "user": user,
                  "passw": passw}
            pcl_msg = ph.base64pickle(msg)
            self.window_id = self.guest_obj.current_window_id
            self.guest_obj.send(
                "application " + "fileTransfer " + str(self.window_id) + " smbCopy " + pcl_msg)
            self.guest_obj.current_window_id += 1

        except Exception as e:
            raise Exception(
                lineno() + " Error: fileTransferVmmSide::__init__ " + self.guest_obj.guestname + " " + str(e))         


    def open(self):
        """Sends a command to open a filetransfer on the associated guest.

        unused as of right now

        """
        try:
            self.logger.info("function: fileTransferVmmSide::open")
            
        except Exception as e:
            raise Exception("error fileTransferVmmSide::open: " + str(e))

    def close(self):
        """Sends a command to close a fileTransfer on the associated guest.
         
         unused as of right now

        """
        try:
            self.logger.info("function: fileTransferVmmSide::close")
        except Exception as e:
            raise Exception("error fileTransferVmmSide:close()" + str(e))


###############################################################################
# Commands to parse on host side
###############################################################################
class FileTransferVmmSideCommands(ApplicationVmmSideCommands):
    """
    Class with all commands for fileTransferVmmSide which will be received from the agent on the guest.

    Static only.

    """

    @staticmethod
    def commands(guest_obj, cmd):
        # cmd[0] = win_id; cmd[1] = state
        module_name = "fileTransfer"
        guest_obj.logger.debug("fileTransferVmmSideCommands::commands: " + cmd)
        cmd = cmd.split(" ")
        try:
            if "opened" in cmd[1]:
                guest_obj.logger.debug("in opened")
                for obj in guest_obj.applicationWindow[module_name]:
                    if cmd[0] == str(obj.window_id):
                        guest_obj.logger.debug("window_id: " + str(obj.window_id) + " found!")
                        guest_obj.logger.info(module_name + " with id: " + str(obj.window_id) + " is_opened = true")
                        obj.is_opened = True
                        guest_obj.logger.debug("browser_obj.is_opened is True now!")

            if "busy" in cmd[1]:
                guest_obj.logger.debug("in busy")
                for obj in guest_obj.applicationWindow[module_name]:
                    if cmd[0] == str(obj.window_id):
                        guest_obj.logger.info(module_name + " with id: " + str(obj.window_id) + " is_busy = true")
                        obj.is_busy = True

            if "ready" in cmd[1]:
                guest_obj.logger.debug("in ready")
                for obj in guest_obj.applicationWindow[module_name]:
                    if cmd[0] == str(obj.window_id):
                        guest_obj.logger.info(module_name + " with id: " + str(obj.window_id) + " is_busy = false")
                        obj.is_busy = False

            if "error" in cmd[1]:
                guest_obj.logger.debug("in error")
                for obj in guest_obj.applicationWindow[module_name]:
                    if cmd[0] == str(obj.window_id):
                        guest_obj.logger.info(module_name + " with id: " + str(obj.window_id) + " has_error = True")
                        obj.has_error = True

        except Exception as e:
            raise Exception(module_name + "_host_side_commands::commands " + str(e))


###############################################################################
# Guest side implementation
###############################################################################
class FileTransferGuestSide(ApplicationGuestSide):
    """fileTransfer implementation of the guest side.

    Usually Windows, Linux guest's

    """

    def __init__(self, agent_obj, logger):
        super(FileTransferGuestSide, self).__init__(agent_obj, logger)
        try:
            self.module_name = "fileTransfer"
            self.timeout = None
            self.window_is_crushed = None
            self.window_id = None
            self.agent_object = agent_obj
            self.helper = None

        except Exception as e:
            raise Exception("Error in " + self.__class__.__name__ +
                            ": " + str(e))
                            
    def smbCopy(self, args):
        """ Copies file to smbshare.
           :param source_file: source file
           :param target_file: target file
           :param user: SMB User
           :param passwd: SMB Password
       """
        ai = ph.base64unpickle(args)

        #sfile = base64.b64decode(source_file)
        #tfile = base64.b64decode(target_file)
        #user = base64.b64decode(user)
        #passwd = base64.b64decode(passwd)
        
        sfile = ai["guest_source_path"]
        tfile = ai["smb_target_path"]
        user=ai["user"]
        passwd=ai["passw"]

        shutil.copy(sfile, tfile, True, username=user, password=passwd)          
    
    def open(self):
        """Sends a command to open a filetransfer on the associated guest.

        unused as of right now

        """
        try:
            self.logger.info("function: fileTransferGuestSide::open")
            
        except Exception as e:
            raise Exception("error fileTransferGuestSide::open: " + str(e))

    def close(self):
        """Sends a command to close a fileTransfer on the associated guest.
         
         unused as of right now

        """
        try:
            self.logger.info("function: fileTransferGuestSide::close")
        except Exception as e:
            raise Exception("error fileTransferGuestSide:close()" + str(e))

                            
                            
###############################################################################
# Commands to parse on guest side
###############################################################################
class FileTransferGuestSideCommands(ApplicationGuestSideCommands):
    """
    Class with all commands for one application.

    call the ask method for an object. The call will be done by a thread, so if the timeout is
    reached, the open application will be closed and opened again.
    Static only.

    """

    @staticmethod
    def commands(agent_obj, obj, cmd):  # commands(obj, cmd) obj from list objlist[window_id] win id in cmd[1]?
        try:
            agent_obj.logger.info("static function fileTransferGuestSideCommands::commands")
            agent_obj.logger.debug("command to parse: " + cmd)
            com = cmd.split(" ")
            if len(com) > 3:
                args = " ".join(com[3:])

            module = com[0]  # inspect.stack()[-1][1].split(".")[0]
            window_id = com[1]
            method_string = com[2]

            method_found = False
            methods = inspect.getmembers(obj, predicate=inspect.ismethod)

            for method in methods:
                # method[0] will now contain the name of the method
                # method[1] will contain the value

                if method[0] == method_string:
                    # start methods as threads
                    method_found = True
                    agent_obj.logger.debug("method to call: " + method[0] + "(" + args + ")")
                    agent_obj.logger.debug("args")
                    tmp_thread = threading.Thread(target=method[1], args=(args,))
                    agent_obj.logger.debug("thread is defined")
                    tmp_thread.start()
                    agent_obj.logger.debug("thread started")
                    tmp_thread.join(50)  # Wait until the thread is completed
                    if tmp_thread.isAlive():
                        agent_obj.logger.error("thread is alive... time outed")
                        # close open tasks (browser...)
                        # Todo close open function and windows
                        agent_obj.logger.info(
                            "fileTransferGuestSideCommands::commands: Close all open browsers and " + "clear the fileTransfer list")
                        #TODO: test
                        for m in methods:
                            if m[0] == "close":
                                m[1]()  # call close method for safe quiting
                        #if platform.system() == "Windows":
                        #    subprocess.call(["taskkill", "/IM", "firefox.exe", "/F"])
                        #elif platform.system() == "Linux":
                        #    os.system("pkill firefox")
                        #else:
                        #    raise NotImplemented("Not implemented for system: " + platform.system())
                        # for browserObject in agent_obj.applicationWindow[module]:
                        #    agent_obj.applicationWindow[module].remove(browserObject)
                        # set a crushed flag.
                        obj.is_opened = False
                        obj.is_busy = False
                        obj.has_error = True

                        agent_obj.logger.info("application " + module + " " + str(window_id) + " error")
                        agent_obj.send("application " + module + " " + str(window_id) + " error")

            if not method_found:
                raise Exception("Method " + method_string + " is not defined!")
        except Exception as e:
            raise Exception("Error in fileTransferGuestSideCommands::commands " + str(e))