# Copyright (C) 2013-2014 Reinhard Stampp
# This file is part of hystck - http://hystck.fbi.h-da.de
# See the file 'docs/LICENSE' for copying permission.

try:
    import logging
    import sys
    import platform
    import threading
    import subprocess
    import inspect  # for listing all method of a class
    import base64

    import cPickle

    # base class VMM side
    from hystck.application.application import ApplicationVmmSide
    from hystck.application.application import ApplicationVmmSideCommands

    #
    import hystck.utility.picklehelper as ph

    # base class guest side
    from hystck.application.application import ApplicationGuestSide
    from hystck.application.application import ApplicationGuestSideCommands
    from hystck.utility.line import lineno

except ImportError as ie:
    print("Import error! in userManagement.py " + str(ie))
    exit(1)


###############################################################################
# Host side implementation
###############################################################################
class UserManagementVmmSide(ApplicationVmmSide):
    """
    This class is a remote control on the host-side to control a real <userManagement>
    running on a guest.
    """

    def __init__(self, guest_obj, args):
        """Set default attribute values only.
        @param guest_obj: The guest on which this application is running. (will be inserted from guest::application())
        @param args: containing
                 logger: Logger name for logging.
        """
        try:
            super(UserManagementVmmSide, self).__init__(guest_obj, args)
            self.logger.info("function: UserManagementVmmSide::__init__")
            self.window_id = None

        except Exception as e:
            raise Exception(lineno() + " Error: UserManagementHostSide::__init__ " + self.guest_obj.guestname + " " + str(e))

    def open(self):
        """Sends a command to open a userManagement on the associated guest.
        """
        try:
            self.logger.info("function: UserManagementVmmSide::open")
            self.window_id = self.guest_obj.current_window_id
            self.guest_obj.send("application " + "userManagement " + str(self.window_id) + " open ")  # some parameters

            self.guest_obj.current_window_id += 1

        except Exception as e:
            raise Exception("error UserManagementVmmSide::open: " + str(e))

    def close(self):
        """Sends a command to close a <userManagement> on the associated guest.
        """
        try:
            self.logger.info("function: UserManagementVmmSide::close")
            self.guest_obj.send("application " + "userManagement " + str(self.window_id) + " close ")
        except Exception as e:
            raise Exception("error UserManagementVmmSide:close()" + str(e))

    def addUser(self, user_name, password):
        """Creating a User on the guest system
        """
        try:
            self.logger.info("function: UserManagementVmmSide:addUser")
            ac = {"usr_name": user_name,
                  "password": password}
            pcl_ac = ph.base64pickle(ac)
            pw_cmd = "application userManagement " + str(self.window_id) + " addUser " + pcl_ac
            self.is_busy = True
            self.guest_obj.send(pw_cmd)
        except Exception as e:
            raise Exception("error UserManagementVmmSide:addUser() " + str(e))


###############################################################################
# Commands to parse on host side
###############################################################################
class UserManagementVmmSideCommands(ApplicationVmmSideCommands):
    """
    Class with all commands for <userManagement> which will be received from the agent on the guest.

    Static only.
    """

    @staticmethod
    def commands(guest_obj, cmd):
        # cmd[0] = win_id; cmd[1] = state
        module_name = "userManagement"
        guest_obj.logger.debug("UserManagementVmmSideCommands::commands: " + cmd)
        cmd = cmd.split(" ")
        try:
            if "opened" in cmd[1]:
                guest_obj.logger.debug("in opened")
                for obj in guest_obj.applicationWindow[module_name]:
                    if cmd[0] == str(obj.window_id):
                        guest_obj.logger.debug("window_id: " + str(obj.window_id) + " found!")
                        guest_obj.logger.info(module_name + " with id: " + str(obj.window_id) + " is_opened = true")
                        obj.is_opened = True
                        guest_obj.logger.debug("obj.is_opened is True now!")

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
class UserManagementGuestSide(ApplicationGuestSide):
    """<userManagement> implementation of the guest side.

    Usually Windows, Linux guest's
    class attributes
    window_id - The ID for the opened object
    """

    def __init__(self, agent_obj, logger):
        super(UserManagementGuestSide, self).__init__(agent_obj, logger)
        try:
            self.module_name = "userManagement"
            self.timeout = None
            self.window_is_crushed = None
            self.window_id = None
            self.agent_object = agent_obj

        except Exception as e:
            raise Exception("Error in " + self.__class__.__name__ +
                            ": " + str(e))

    def open(self, args):
        """
        Open a <userManagement> and save the userManagement object with an id in a dictionary.
        Set page load timeout to 30 seconds.

        return:
        Send to the host in the known to be good state:
        'application <userManagement> window_id open'.
        'application <userManagement> window_id ready'.
        in the error state:
        'application <userManagement> window_id error'.
        additionally the 'window_is_crushed' attribute is set; so the next
        call will open a new window.

        """
        try:
            arguments = args.split(" ")
            var = arguments[0]
            var2 = arguments[1]

            self.logger.info(self.module_name + "GuestSide::open")
            if var == "type":
                self.logger.debug("wait for start UserManagement...")
                # start application <skeletion>
                self.logger.debug("started!")
            elif var == "type2":
                self.logger.debug("wait for start UserManagement...")
                # start application <skeletion>
                self.logger.debug("started!")
            else:
                self.logger.error("skeletion type " + var +
                                  " not implemented")
                return

            # send some information about the userManagement state
            self.agent_object.send("application " + self.module_name + " " + str(self.window_id) + " opened")

            self.agent_object.send("application " + self.module_name + " " + str(self.window_id) + " ready")
            self.window_is_crushed = False
        except Exception as e:
            self.logger.info("UserManagementGuestSide::open: Close all open windows and clear the userManagement list")
            subprocess.call(["taskkill", "/IM", "userManagement.exe", "/F"])
            # for obj in self.agent_object.applicationWindow[self.module_name]:
            #    self.agent_obj.applicationWindow[self.module_name].remove(obj)
            # set a crushed flag.
            self.window_is_crushed = True
            self.agent_object.send("application " + self.module_name + " " + str(self.window_id) + " error")
            self.logger.error("Error in " + self.__class__.__name__ + "::open" + ": selenium is crushed: " + str(e))

    def close(self):
        """Close one given window by window_id"""
        self.logger.info(self.__class__.__name__ +
                         "::close ")
        self.seleniumDriver.quit()

    def addUser(self, args):
        """add User to guest"""
        self.logger.info(self.__class__.__name__ +
                         "::addUser ")
        ad = ph.base64unpickle(args)

        ################
        user = ad["usr_name"]
        password = ad["password"]
        #################

        if platform.system() == "Windows":
            cmd = base64.b64encode('net user ' + user + ' ' + password + ' /ADD')
            try:
                #self.agent_object.do_command("runElevated " + cmd)
                subprocess.call(["net", "user", user, password, "/ADD"])
            except Exception as e:
                self.logger.error("adding user failed: " + lineno() + ' ' + str(e))
        else:
            self.logger.error("Unknown System Platform, only Windows is supported at the moment")


###############################################################################
# Commands to parse on guest side
###############################################################################
class UserManagementGuestSideCommands(ApplicationGuestSideCommands):
    """
    Class with all commands for one application.

    call the ask method for an object. The call will be done by a thread, so if the timeout is
    reached, the open application will be closed and opened again.
    Static only.
    """

    @staticmethod
    def commands(agent_obj, obj, cmd):  # commands(obj, cmd) obj from list objlist[window_id] win id in cmd[1]?
        try:
            agent_obj.logger.info("static function UserManagementGuestSideCommands::commands")
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
                        # close userManagement and set obj to crashed
                        agent_obj.logger.error("thread is alive... time outed")
                        agent_obj.logger.info(
                            "UserManagementGuestSideCommands::commands: Close all open windows and " + "clear the userManagement list")
                        subprocess.call(["taskkill", "/IM", "userManagement.exe", "/F"])
                        for obj in agent_obj.applicationWindow[module]:
                            agent_obj.applicationWindow[module].remove(obj)
                        # set a crushed flag.
                        obj.is_opened = False
                        obj.is_busy = False
                        obj.has_error = True

                        agent_obj.logger.info("application " + module + " " + str(window_id) + " error")
                        agent_obj.send("application " + module + " " + str(window_id) + " error")

            if not method_found:
                raise Exception("Method " + method_string + " is not defined!")
        except Exception as e:
            raise Exception("Error in UserManagementGuestSideCommands::commands " + str(e))
