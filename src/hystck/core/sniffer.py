import logging
import os
import subprocess
import time
from os.path import join

import hystck.utility.constants as constants
from hystck.utility.logger_helper import create_logger


class Sniffer:
    def __init__(self, name, hypervisor_ip, hypervisor_userAtHost,
                 path='/usr/sbin/tcpdump',
                 logger=None):
        self.name = name
        self.hypervisor_ip = hypervisor_ip
        self.hypervisor_userAtHost = hypervisor_userAtHost
        self.path = path
        self.process = None
        if logger is None:
            self.logger = create_logger(name, logging.INFO)
        else:
            self.logger = logger

    def start(self):
        try:
            network_dump_hypervisor_path = join(constants.FILEPATH_NETWORK_DUMPS, self.hypervisor_ip)
            network_dump_guest_path = join(network_dump_hypervisor_path, self.name)
            network_dump_file_path = join(network_dump_guest_path, str(int(time.time())) + ".pcap")

            # setup dump directory structure
            if not os.path.exists(network_dump_hypervisor_path):
                os.mkdir(network_dump_hypervisor_path)

            if not os.path.exists(network_dump_guest_path):
                os.mkdir(network_dump_guest_path)

            self.process = subprocess.Popen(
                [self.path, "-i", constants.NETWORK_INTERNET_BRIDGE_INTERFACE, "-w", network_dump_file_path, "-s0"])
            self.logger.info("sniffer {} started".format(self.name))
        except Exception as e:
            self.logger.error("sniffer {} failed: ".format(self.name, str(e)))

    def stop(self):
        if self.process:
            # TODO probably sending a sigint is better
            self.process.kill()
            self.logger.info("sniffer {} stopped".format(self.name))
