import argparse
import logging
import random
import time

from hystck.core.vmm import GuestListener
from hystck.core.vmm import Vmm
from hystck.generator import Generator
from hystck.utility.logger_helper import create_logger


def cli():
    parser = argparse.ArgumentParser(description='Haystack generator utility.')
    parser.add_argument(
        'config_file',
        type=str,
        help='path to the config file'
    )
    parser.add_argument(
        '--guest',
        type=str,
        help='name of the guest virtual machine',
        nargs='?',
        default='guest'
    )
    parser.add_argument(
        '--seed',
        type=int,
        help='initial seed to use for random number generation',
        nargs='?',
        default=None
    )

    args = parser.parse_args()

    # Seed the random number generator
    random.seed(args.seed)

    # Create virtual machine.
    macs_in_use = []
    guests = []

    logger = create_logger('haystack_generator', logging.DEBUG)
    guest_listener = GuestListener(guests, logger)
    virtual_machine_monitor = Vmm(macs_in_use, guests, logger)
    guest = virtual_machine_monitor.create_guest(guest_name=args.guest_name, platform="windows")

    # Waiting to connect to guest.
    logger.debug("[~] Trying to connect to guest.")

    while guest.state != "connected":
        logger.debug(".")
        time.sleep(1)

    logger.debug('[+] Connected to %s', guest.guestname)

    # Load and parse config file.
    generator = Generator(guest, args.config_file, logger)

    # Execute action suite.
    generator.execute()

    # Shutdown the generator before closing the VM.
    generator.shutdown()

    # Shutdown virtual machine but keep the disk.
    guest.shutdown('keep')
