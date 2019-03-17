# Copyright (C) 2013-2014 Reinhard Stampp
# Copyright (C) 2017 Sascha Kopp
# This file is part of hystck - http://hystck.fbi.h-da.de
# See the file 'docs/LICENSE' for copying permission.

import sys
import socket
import time
import logging
import base64
import subprocess
import platform
import datetime
import os
import zipfile
from threading import Lock, Thread, Condition

import shutil
import psutil

import StringIO

if platform.system() == "Windows":
    import win32api
    import pywintypes
    import cPickle
    from hystck.utility.winmessagepipe import WinMessagePipe

try:
    from hystck.utility.logger_helper import create_logger
    from hystck.utility.network import NetworkInfo
except ImportError as ie:
    raise Exception("agent " + str(ie))


class Agent(object):
    """hystck agent, it runs inside guest; i.e. Windows 7 or Linux:


    """

    def __init__(self, operating_system="windows", logger=None):
        try:
            self._send_lock = Lock()
            self._pexec_threads = dict()
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.last_driven_url = ""
            self.window_is_crushed = False
            self.disconnectedByHost = False
            self.operatingSystem = operating_system
            self.applicationWindow = {}

            self.logger = logger
            if self.logger is None:
                self.logger = create_logger('agent', logging.DEBUG)

            # - TODO: add support for linux
            if operating_system == "Windows":
                from hystck.inputDevice.inputDevice import InputDeviceManagement
                self.inputDeviceManager = InputDeviceManagement(self, logger)

            # open pipe for Windows admin commands
            if platform.system() == "Windows":
                self.adminpipe = WinMessagePipe()
                self.adminpipe.open("hystckadmin", mode='w')

            self.logger.debug("agent::init finished")
        except Exception as e:
            raise Exception("Agent::init error: " + str(e))

    def connect(self, host, port):
        """After creation of this object, this method will connect to the vmm"""
        while 1:
            try:
                self.logger.debug("try to connect...")
                self.sock.connect((host, port))
                if self.sock != 0:
                    break
                self.logger.debug("connected")
            except:
                time.sleep(1)
                self.logger.error("Error: can't connect to host " + host + ":" + str(port))

    def register(self):
        ip_local = NetworkInfo.get_local_IP()
        ip_internet = NetworkInfo.get_internet_IP()
        mac = NetworkInfo.get_MAC()
        internet_iface = NetworkInfo.get_internet_interface()
        local_iface = NetworkInfo.get_local_interface()
        self.send("register " + str(ip_internet) + " " + str(ip_local) + " " + str(
            mac) + " " + internet_iface + " " + local_iface)

    def do_command(self, command):
        """Check for keywords in 'command'

        Keywords:
          application <string to parse>

          inputDevice <string to parse>

          destroyConnection

        """
        try:
            self.logger.info("Agent::do_command")
            self.logger.debug("command: " + command)
            com = command.split(" ")

            package = com[0]

            if "application" in package:
                module = com[1]
                window_id = com[2]
                if len(com) > 4:
                    args = " ".join(com[4:])

                self.logger.debug("before loading module")
                # load class moduleGuestSide and moduleGuestSideCommands
                name = "hystck." + package + "." + module
                self.logger.debug("module to load: " + name)
                mod = __import__(name, fromlist=[''])
                self.logger.debug("module '" + module + "' will be loaded via __import__")
                class_commands = getattr(mod, module[0].upper() + module[1:] + 'GuestSideCommands')
                self.logger.debug("module '" + module + "' is loaded via __import__")
                if module not in self.applicationWindow.keys():
                    self.logger.debug("module '" + module + "' not in applicationWindow -> do add")
                    self.applicationWindow[module] = []

                window_exists = False
                for app_obj in self.applicationWindow[module]:
                    # call it's method
                    if app_obj.window_id is window_id:
                        self.logger.debug("module '" + module + "' with window " + str(window_id) + " exists")
                        window_exists = True
                        class_commands.commands(self, app_obj, " ".join(com[1:]))
                        self.logger.debug("mod_commands.commands are called")

                if not window_exists:
                    # create a new object
                    self.logger.debug("no window exists")
                    self.logger.debug("to create one, load module " + module + "GuestSide")
                    mod = __import__(name, fromlist=[''])
                    class_guest_side = getattr(mod, module[0].upper() + module[1:] + 'GuestSide')

                    self.logger.debug("create an instance")
                    app_obj = class_guest_side(self, self.logger)  # (agent_object, logger)
                    self.logger.debug("set window_id " + str(window_id))
                    app_obj.window_id = window_id
                    # process command string and call appropriate method
                    self.logger.debug("mod_commands.call commands")
                    class_commands.commands(self, app_obj, " ".join(com[1:]))
                    self.logger.debug("mod_commands.commands are called")
                    self.applicationWindow[module].append(app_obj)
                    self.logger.debug("object is appended to the applicationWindow[module] list")

            elif "inputDevice" in package:
                """call the execution method from the inputDevice manager"""
                if len(com) < 2:
                    self.logger.error("inputDevice need one parameter: " + str(len(com) - 1) + " given")
                    return

                if self.operatingSystem != "Windows":
                    raise NotImplementedError("InputDeviceManagement is only implemented for windows by now")

                self.inputDeviceManager.execute(" ".join(com[1:]))

            elif "shellExec" in package:
                """decode and execute a command in the system shell"""
                cv = Condition()
                registered = [False]
                shell_exec_id = int(com[1])
                cmd = base64.b64decode(com[2])
                path_prefix = base64.b64decode(com[3])
                if len(com) == 5:
                    std_in = base64.b64decode(com[4])
                else:
                    std_in = ""
                t = Thread(target=self._do_shell_exec,
                           kwargs={"shell_exec_id": shell_exec_id, "cmd": cmd, "path_prefix": path_prefix,
                                   "std_in": std_in, "condition": cv, "registered": registered})
                self._pexec_threads[shell_exec_id] = (t, None)  # save thread handles
                t.start()
                while not registered[0]:
                    with cv:
                        cv.wait()

            elif "remoteShellExec" in package:
                """copies file to vm and executes it in the system shell"""
                cv = Condition()
                registered = [False]
                shell_exec_id = int(com[1])
                filename = base64.b64decode(com[2])
                file = base64.b64decode(com[3])
                target_dir = base64.b64decode(com[4])
                path_prefix = target_dir
                if target_dir == "#unset":
                    target_dir = ""
                if len(com) == 6:
                    std_in = base64.b64decode(com[5])
                else:
                    std_in = ""
                try:
                    with open(target_dir + filename, 'wb') as f:
                        f.write(file)
                except IOError:
                    self.logger.error("File not writable: " + filename)
                t = Thread(target=self._do_shell_exec,
                           kwargs={"shell_exec_id": shell_exec_id, "cmd": filename, "path_prefix": path_prefix,
                                   "std_in": std_in, "condition": cv, "registered": registered})
                self._pexec_threads[shell_exec_id] = (t, None)  # save thread handles
                t.start()
                while not registered[0]:
                    with cv:
                        cv.wait()

            elif "killShellExec" in package:
                """kill previously started process via intern handle id"""
                handle = None
                ishell_exec_id = int(com[1])
                self.logger.debug("Trying to kill process with internal id: " + com[1])
                try:
                    handle = self._pexec_threads[ishell_exec_id][1]  # type: subprocess.Popen
                    if handle is not None:
                        # handle.kill()
                        p = psutil.Process(pid=handle.pid)
                        cs = p.children(recursive=True)
                        for c in cs:
                            c.kill()
                        p.kill()
                    else:
                        self.logger.critical(
                            "This process id has no handle. This should not happen! [" + str(ishell_exec_id) + "]")
                except KeyError:
                    self.logger.error("The specified handle id was not found: " + str(ishell_exec_id))
                except:
                    self.logger.error(
                        "Failed to kill process with handle_id/pid: " + str(ishell_exec_id) + "/" + handle.pid)

            elif "file" in package:
                fcmd = com[1]
                if "filecopy" in fcmd:
                    tname = base64.b64decode(com[2])
                    file = base64.b64decode(com[3])
                    self._filecopy(tname, file)
                elif "dircopy" in fcmd:
                    tdir = base64.b64decode(com[2])
                    zfile = base64.b64decode(com[3])
                    self._dircopy(tdir, zfile)
                elif "dircreate" in fcmd:
                    tdir = base64.b64decode(com[2])
                    self._dircreate(tdir)
                elif "touch" in fcmd:
                    tfile = base64.b64decode(com[2])
                    self._touchfile(tfile)
                elif "guestcopy" in fcmd:
                    sfile = base64.b64decode(com[2])
                    tfile = base64.b64decode(com[3])
                    self._guestcopy(sfile, tfile)
                elif "guestmove" in fcmd:
                    sfile = base64.b64decode(com[2])
                    tfile = base64.b64decode(com[3])
                    self._guestmove(sfile, tfile)
                elif "guestdelete" in fcmd:
                    tpath = base64.b64decode(com[2])
                    self._guestdelete(tpath)
                elif "guestchdir" in fcmd:
                    cpath = base64.b64decode(com[2])
                    self._guestchdir(cpath)
                else:
                    self.logger.warning("Unrecognized file command: " + fcmd)

            elif "setOSTime" in package:
                """set the OSes time"""
                ptime = base64.b64decode(com[1])
                local_time = com[2]
                if local_time == "True":
                    blocal_time = True
                else:
                    blocal_time = False
                try:
                    msg = {"cmd": "setostime", "param": [ptime, local_time]}
                    msg = cPickle.dumps(msg)
                    self.adminpipe.write(msg)
                except cPickle.PickleError:
                    self.logger.error("Cannot pickle command data!")
                except OSError:
                    self.logger.warning("Sending command to supplementary Agent failed, using fallback!")
                    self._set_os_time(ptime, blocal_time)

            elif "runElevated" in package:
                self.logger.debug("agent runElevated")
                command = base64.b64decode(com[1])
                try:
                    msg = {"cmd": "runelevated", "param": [command]}
                    msg = cPickle.dumps(msg)
                    self.logger.debug("msg: " + msg)
                    self.adminpipe.write(msg)
                except cPickle.PickleError:
                    self.logger.warning("Cannot pickle command data!")
                except OSError:
                    self.logger.warning("Sending command to supplementary Agent failed!")

            elif "cleanUp" in package:
                '''
                added by Thomas Schaefer in 2019, reducing artefacts left by hystck
                '''
                self.logger.debug("agent cleanUp")
                command = base64.b64decode(com[1])
                try:
                    import subprocess
                    import os
                    # cleaning registry entries
                    if(platform.system() == "Windows"):
                        os.system('reg delete \"HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\OpenSavePidlMRU\\py\"  /f')
                        os.system('reg delete \"HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\ComDlg32\\OpenSavePidlMRU\\pyc\"  /f')
                    # cleaning filesystem
                    # os.system("rmdir /s /q C:\\Users\\Bill\\Desktop\\hystck")
                    os.system("rmdir /s /q C:\\Python27\\Lib\\site-packages\\hystck")
                except OSError:
                    self.logger.warning("Executing commands failed.")

            elif "destroyConnection" in com[0]:
                self.disconnectedByHost = True
                self.destroyConnection()

            else:
                self.logger.error("command " + com[0] + " not found!")
        except Exception as e:
            self.logger.error(str(e))

    def _do_shell_exec(self, shell_exec_id, cmd, path_prefix, std_in, condition, registered):
        """ Actually run shellExec.

        :type registered: list
        :type condition: Condition
        :param registered: Condition for condition variable
        :param condition: A condition variable to notify setting of handle
        :param shell_exec_id: id of this call
        :param cmd: the command to execute
        :param path_prefix: a path that should be prefixed to cmd
        :param std_in: text input for interactive console programs
        """
        # wtf is this stuff doing here
        # if platform.system() == "Windows":
        #    subprocess.call(["taskkill", "/IM", "firefox.exe", "/F"])
        # elif platform.system() == "Linux":
        #    os.system("pkill firefox")
        # else:
        #    raise NotImplemented("Not implemented for system: " + platform.system())
        if path_prefix != "#unset":
            if sys.platform == "win32":
                cmd = path_prefix + "\\" + cmd
            else:
                cmd = path_prefix + "/" + cmd
        try:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 stdin=subprocess.PIPE)
            self._pexec_threads[shell_exec_id] = (self._pexec_threads[shell_exec_id][0], p)  # save handle to allow kill
        except:
            pass
        finally:
            registered[0] = True
            with condition:
                condition.notifyAll()
        std_out, std_err = p.communicate(input=std_in)
        exit_code = p.returncode
        std_out = base64.b64encode(std_out)  # base64 encode to avoid fragmentation
        std_err = base64.b64encode(std_err)  # base64 encode to avoid fragmentation
        self.send("shellExecComplete " + str(shell_exec_id) + " " + str(exit_code) + " " + std_out + " " + std_err)

    def _set_os_time(self, ptime, local_time=True):
        """ Sets the systems time to the specifies date
            This may need admin rights on Windows

            :type local_time: bool
            :type ptime: str
            :param ptime: a posix date string in format "%Y-%m-%d %H:%M:%S"
            :param local_time: is this local time

        """
        try:
            t = time.strptime(ptime, "%Y-%m-%d %H:%M:%S")
            self.logger.info("Trying to set time to: " + ptime)
        except ValueError:
            self.logger.error("Bad datetime format")
            return
        if platform.system() == "Windows":
            try:
                if local_time:
                    wt = pywintypes.Time(t)
                    rval = win32api.SetLocalTime(wt)  # you may prefer localtime
                else:
                    rval = win32api.SetSystemTime(t[0], t[1], t[6], t[2], t[3], t[4], t[5], 0)
                if rval == 0:
                    self.logger.error("Setting system time failed - function returned 0 - error code is {0}".format(
                        str(win32api.GetLastError())))
            except win32api.error:
                self.logger.error("Setting system time failed due to exception!")
        elif platform.system() == "Linux":
            pass  # todo: implement
        else:
            pass  # everything else unsupported

    def destroyConnection(self):
        """ Close the socket

        Will close the open socket to the  and end the
        """
        try:
            self.sock.close()
            self.logger.info("interactionmanager end!")
            sys.exit(0)
        except Exception as e:
            logging.error("destroyConnection - Error:" + str(e))

    def send(self, msg):
        """Forward messages to the vmm"""
        self._send_lock.acquire()  # prevent parallel sending from multiple threads
        message_size = "%.8x" % len(msg)
        buffer = message_size + msg
        self.logger.debug("sent: " + buffer)
        sent = self.sock.send(buffer)
        if sent == 0:
            self._send_lock.release()
            raise RuntimeError("socket connection broken")
        else:
            self._send_lock.release()

    def receiveCommands(self):
        """receive commands from the vmm in an infinite loop"""
        msg = ""
        allreceived = False
        try:
            # try long as there are unfinished received commands
            while 1:
                if allreceived:
                    break
                if self.disconnectedByHost:
                    break
                chunk = self.sock.recv(1024)
                if chunk == '':
                    raise RuntimeError("socket connection broken")
                # get length of the message
                # self.logger.error("complete chunk: " + chunk)
                msg = msg + chunk
                # if msg do not contain the message length
                if len(msg) < 8:
                    self.logger.error("half command")
                    continue

                message_size = int(msg[0:8], 16)

                if len(msg) < (message_size + 8):
                    continue

                # get the commands out of the message
                while len(msg) >= (message_size + 8):
                    # if the command fit into message, return the command list commands
                    if len(msg) == message_size + 8:
                        self.do_command(msg[8:(message_size + 8)])
                        msg = ""
                        allreceived = True
                        break
                    # there are multiple commands in the message
                    else:
                        if len(msg) < (message_size + 8):
                            continue

                        command = msg[8:(message_size + 8)]
                        msg = msg[(message_size + 8):]

                        message_size = int(msg[0:8], 16)
                        self.do_command(command)
        except Exception as e:
            self.logger.error("error recv: " + str(e))

        return

    def _filecopy(self, target_name, file_content):
        """ Writes a file to disk.

        :param target_name: filename to write to
        :param file_content: content of file
        """
        self.logger.debug("File receive to: " + str(target_name))
        with open(target_name, 'wb') as f:
            f.write(file_content)

    def _dircopy(self, target_directory, zip_file):
        """ Writes a directory to disk.

        :param target_directory: unpack path
        :param zip_file: string containing a zip-file
        """
        self.logger.debug("Directory receive to: " + str(target_directory))
        zbuf = StringIO.StringIO()
        zbuf.write(zip_file)
        z = zipfile.ZipFile(zbuf)
        z.extractall(target_directory)
        z.close()
        zbuf.close()

    def _dircreate(self, target_directory):
        """ Creates a directory.

        :param target_directory: directory path to create
        """
        self.logger.debug("Create directoty at: " + str(target_directory))
        os.mkdir(target_directory)

    def _touchfile(self, target_path):
        """ Touches a file.

        :param target_path: file to touch
        """
        self.logger.debug("Touching file at: " + str(target_path))
        with open(target_path, 'a'):
            os.utime(target_path, None)

    def _guestcopy(self, source_file, target_file):
        """ Copies file.

        :param source_file: source file
        :param target_file: target file
        """
        self.logger.debug("Copying file from: " + str(source_file) + " To: " + str(target_file))
        shutil.copy(source_file, target_file)

    def _guestmove(self, source_file, target_file):
        """ Moves file.

        :param source_file: source file
        :param target_file: target file
        """
        self.logger.debug("Moving file from: " + str(source_file) + " To: " + str(target_file))
        shutil.move(source_file, target_file)

    def _guestdelete(self, target_path):
        """ Delete file or directory on guest.

        :param target_path: file or directory to delete
        """
        self.logger.debug("Deleting file at: " + str(target_path))
        if os.path.isdir(target_path):
            shutil.rmtree(target_path, True)
        else:
            os.remove(target_path)

    def _guestchdir(self, new_path):
        """ Changes the current working directory.

        :param new_path: New current working directory
        """
        os.chdir(new_path)
