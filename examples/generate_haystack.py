import argparse
import logging
import time
from hystck.utility.logger_helper import create_logger
from hystck.generator import Generator
from hystck.core.vmm import Vmm
from hystck.core.vmm import GuestListener


def main():
    # Create logger.
    logger = create_logger('haystack_generator', logging.DEBUG)

    # Parse command line arguments.
    parser = argparse.ArgumentParser(description='Haystack generator utility.')
    parser.add_argument('guest_name', type=str, help='name of the guest virtual machine', nargs='?',
                        default='guest')
    parser.add_argument('config_file', type=str, help='path to the config file', nargs='?',
                        default='example-haystack.yaml')

    args = parser.parse_args()

    # Create virtual machine.
    macs_in_use = []
    guests = []

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


if __name__ == "__main__":
    main()
