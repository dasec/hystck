import argparse
import logging
import time
import threading

from hystck.utility.logger_helper import create_logger
from hystck.generator import Generator
from hystck.core.vmm import Vmm
from hystck.core.vmm import GuestListener

# Create logger for the Haystack core and generator.
logger_core = create_logger('haystack_core', logging.ERROR)
logger_generator = create_logger('haystack_generator', logging.DEBUG)


def start_guest(index, virtual_machine_monitor, args):
    guest = virtual_machine_monitor.create_guest(guest_name='{}-{}'.format(args.guest, index), platform="windows")

    # Waiting to connect to guest.
    logger_generator.info('[~] Trying to connect to guest {}.'.format(index))

    while guest.state != "connected":
        logger_generator.debug(".")
        time.sleep(1)

    logger_generator.info('[+] Connected to %s', guest.guestname)

    # Load and parse config file.
    generator = Generator(guest, args.config_file, logger_generator, args.seed)

    # Execute action suite.
    generator.execute()

    # Shutdown the generator before closing the VM.
    generator.shutdown()

    # Shutdown virtual machine but keep the disk.
    guest.shutdown('keep')


def main():
    # Parse command line arguments.
    parser = argparse.ArgumentParser(description='Haystack generator utility.')
    parser.add_argument('config_file', type=str, help='path to the config file')
    parser.add_argument('--guest', type=str, help='name of the guest virtual machine', nargs='?',
                        default='guest-{}'.format(int(time.time())))
    parser.add_argument('--seed', type=int, help='initial seed to use for random number generation', nargs='?',
                        default=None)
    parser.add_argument('--parallel', type=int, help='amount of virtual machines running parallel', nargs='?',
                        default=1)

    args = parser.parse_args()

    # Create virtual machine.
    macs_in_use = []
    guests = []

    guest_listener = GuestListener(guests, logger_core)
    virtual_machine_monitor = Vmm(macs_in_use, guests, logger_core)

    for index in range(0, args.parallel):
        thread = threading.Thread(target=start_guest, args=(index, virtual_machine_monitor, args))
        thread.start()
        thread.join()


if __name__ == "__main__":
    main()
