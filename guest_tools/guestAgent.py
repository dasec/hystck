# Copyright (C) 2013-2014 Reinhard Stampp
# This file is part of hystck - http://hystck.fbi.h-da.de
# See the file 'docs/LICENSE' for copying permission.


import sys
import time
import logging
import platform

from hystck.core.agent import Agent
from hystck.utility.logger_helper import create_logger


HYSTCK_CONTROLLER_IP = '192.168.102.1'
HYSTCK_CONTROLLER_PORT = 11000

def main():
    # create logger
    logger = create_logger('guestAgent', logging.DEBUG)

    logger.info("create Agent")
    a = Agent(operating_system=platform.system().lower(), logger=logger)
    logger.info("connect to hystck controller: %s:%i" % (HYSTCK_CONTROLLER_IP, HYSTCK_CONTROLLER_PORT))
    a.connect(HYSTCK_CONTROLLER_IP, HYSTCK_CONTROLLER_PORT)

    # let all network interfaces come up
    time.sleep(15)

    # inform hystck controller about network configuration
    a.register()

    # wait for commands
    while 1:
        time.sleep(1)
        a.receiveCommands()


if __name__ == "__main__":
    main()
