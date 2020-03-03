#!/usr/bin/python3
import sys
import os
import logging
import json
import subprocess


class Installer:
    """
    This class is used to install all prerequisites that are needed for hystck. Additionally all paths and privileges
    that hystck needs are created.
    """
    requ = "."
    logger = ""
    param = ""
    general = ""
    tcpdump = ""
    virtpools = ""
    netifaces = ""

    def __init__(self, logger, param):
        self.logger = logger
        self.param = param

    def load_config(self):
        """
        Load config file and read different sections into variables
        :return:
        """
        self.logger.info("[~] Loading configuration...")
        try:
            with open('config.json') as json_data_file:
                data = json.load(json_data_file)
                self.general = data['general']
                self.tcpdump = data['tcpdump']
                self.virtpools = data['libvirt-pools']
                self.netifaces = data['network-interfaces']
        except ValueError, e:
            self.logger.info("[X] Error while reading config file.")
            self.logger.error(e)
            sys.exit(1)
        else:
            self.logger.info("[+] Done loading configuration.")

    def install_apt(self):
        """
        Reads a file of all required packages and installs them through apt-get.
        :return:
        """
        self.logger.info("[~] Installing packet requirements over 'apt'...")
        try:
            aptCmd = "apt-get --yes install {}"
            packetDepFile = os.path.join(self.requ, self.general['packet-requirements'])
            with open(packetDepFile, "r") as file:
                for line in file:
                    prepCmd = aptCmd.format(line.strip())
                    self.logger.debug("Running: {}".format(prepCmd))
                    subprocess.call(prepCmd.split(), stdout=subprocess.PIPE)
        except OSError, e:
            self.logger.info("[X] Error while installing packet requirements.")
            self.logger.error(e)
            sys.exit(1)
        else:
            self.logger.info("[+] Installed 'apt' packet requirements.")

    def install_pip(self):
        """
        Reads a file of all required pip packages and installs them through pip install.
        :return:
        """
        self.logger.info("[~] Installing pip requirements...")
        try:
            pipCmd = "pip install -U {}"
            pipDepFile = os.path.join(self.requ, self.general['pip-requirements'])
            with open(pipDepFile, "r") as file:
                for line in file:
                    prepCmd = pipCmd.format(line.strip())
                    self.logger.debug("Running: {}".format(prepCmd))
                    subprocess.call(prepCmd.split(), stdout=subprocess.PIPE)
        except OSError, e:
            self.logger.info("[X] Error while installing pip packages.")
            self.logger.error(e)
            sys.exit(1)
        else:
            self.logger.info("[+] Successfuly installed pip requirements.")

    def setup_tcpdump(self):
        """
        Setup tcpdump user rights.
        :return:
        """
        self.logger.info("[~] Setting up tcpdump...")
        try:
            prepCmd = "setcap cap_net_raw,cap_net_admin=eip {}".format(self.tcpdump['path'])
            subprocess.call(prepCmd.split(), stdout=subprocess.PIPE)
        except OSError, e:
            self.logger.info("[X] Error setting up tcpdump")
            self.logger.error(e)
            sys.exit(1)
        else:
            self.logger.info("[+] Setting up tcpdump.")

    def setup_libivrt(self):
        """
        Adding groups and rights for libvirt as well as creating disk pools to work with.
        :return:
        """
        self.logger.info("[~] Adding disk pools for libvirt...")
        try:
            commands = ["groupadd libvirtd",
                        "usermod -a -G libvirtd {}".format(self.general['user']),
                        "mkdir {}".format(self.virtpools['path']),
                        "virsh pool-define-as hystck-pool dir - - - - {}/{}".format(self.virtpools['path'],
                                                                                    self.virtpools['name']),
                        "virsh pool-build {}".format(self.virtpools['name']),
                        "virsh pool-start {}".format(self.virtpools['name']),
                        "virsh pool-autostart {}".format(self.virtpools['name'])]
            for command in commands:
                prepCmd = command.strip()
                subprocess.call(prepCmd.split(), stdout=subprocess.PIPE)
        except OSError, e:
            self.logger.info("[X] Error while adding disk pools.")
            self.logger.error(e)
            sys.exit(1)
        else:
            self.logger.info("[+] Added disk pools for libvirt.")

    def setup_network_interfaces(self):
        """
        Sets up the needed network interfaces to later communicate with the vm.
        :return:
        """
        self.logger.info("[~] Adding network interfaces...")
        try:
            commands = ["virsh net-define {}".format(self.netifaces['public-interface-config-file']),
                        "virsh net-define {}".format(self.netifaces['private-interface-config-file']),
                        "virsh net-start {}".format(self.netifaces['public-interface-name']),
                        "virsh net-start {}".format(self.netifaces['private-interface-name']),
                        "virsh net-autostart {}".format(self.netifaces['public-interface-name']),
                        "virsh net-autostart {}".format(self.netifaces['private-interface-name'])]
            for command in commands:
                prepCmd = command.strip()
                subprocess.call(prepCmd.split(), stdout=subprocess.PIPE)
        except OSError, e:
            self.logger.info("[X] Error while adding network interfaces.")
            self.logger.error(e)
            sys.exit(1)
        else:
            self.logger.info("[+] Added network interfaces.")

    def run(self):
        """
        Here all functions for a full installation are called.
        :return:
        """
        self.load_config()
        self.install_apt()
        self.install_pip()

        # Check if installation is host or vm side
        if self.param == "host":
            self.setup_tcpdump()
            self.setup_libivrt()
            self.setup_network_interfaces()

            # Reboot to enable virt-manager user privileges
            # Python2.7: raw_input(); Python3.7: input()
            answer = raw_input('System needs to be restarted for the changes to take effect. '
                               'Do you want to restart now?: [y/n]')
            if not answer or answer[0].lower() != 'y':
                print('You did not indicate approval')
                exit(1)
            else:
                os.system("reboot")
        elif self.param == "vm":
            self.logger.info("[X] Nothing to do inside vm.")
        else:
            self.logger.error("[X] Unknown Parameter {}".format(self.param))


def is_admin():
    """
    Determine if script is running as admin/root
    :return:
    """
    try:
        import os
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


def create_logger():
    """
    Create a logger for sophisticated console output
    :return:
    """
    logger = logging.getLogger("hystck-Installer")
    logger.setLevel(logging.DEBUG)
    fmttr = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%Y.%m.%d %H:%M:%S")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(fmttr)
    logger.addHandler(handler)
    return logger


def main():
    """
    Main Program where instantiations take place and necessary checks and validations are done.
    :return:
    """
    logger = create_logger()

    # stop script if you are not admin
    if not is_admin():
        logger.critical("You are not an admin. Run the installation as admin/root.")
        sys.exit(1)

    # Check Command Line parameter, if none is given set to "vm"
    param = sys.argv[1] if len(sys.argv) >= 2 else "vm"

    installer = Installer(logger, param)

    # Run actual installation
    installer.run()


if __name__ == '__main__':
    main()
