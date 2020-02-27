#!/usr/bin/python3
#test
import sys
import os
import logging
import platform

pip_requ_file = "PIP_requirements.txt"
packet_requ_file = "packet_requirements.txt"

requ = "."
#requ = "Y:\Dokumente\git\hystck"            # just for development stuff

# is current script user an admin / root
def isAdmin():
    try:
        import os
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


def main():
    if len(sys.argv) >= 2:
        param = sys.argv[1]
    else:
        param = "vm"
    
    # Logger Stuff
    logger = logging.getLogger("hystck-Installer")
    logger.setLevel(logging.DEBUG)
    fmttr = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%Y.%m.%d %H:%M:%S")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(fmttr)
    
    logger.addHandler(handler)
    logger.debug("test")
    
    # stop script if you are no admin
    if not isAdmin():
        logger.critical("You are not an admin. Run the installation as admin.")
        sys.exit(1)
        
    # Install required packages
    aptCmd = "apt-get --yes install {}"
    packetDepFile = os.path.join(requ, packet_requ_file)
    with open(packetDepFile, "r") as file:
        for line in file:
            prepCmd = aptCmd.format(line.strip())
            logger.debug("Running: {}".format(prepCmd))
            os.system(prepCmd)
    
    # Install pip dependencies
    pipCmd = "pip install -U {}"
    pipDepFile = os.path.join(requ, pip_requ_file)
    with open(pipDepFile, "r") as file:
        for line in file:
            prepCmd = pipCmd.format(line.strip())
            logger.debug("Running: {}".format(prepCmd))
            os.system(prepCmd)
    
    # Alternatve
    #inst_pip_requirements_cmd = "pip install -U --requirement {}".format(pip_requ_file)
    #logger.debug("Install pip requirement: {}".format(inst_pip_requirements_cmd))
    #os.system(inst_pip_requirements_cmd)
    
    # Setup tcpdump user rights
    os.system("setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump")

    # Check if installation is host or vm side
    if param == "host":
        # Add Pools for Libvirt
        logger.info("adding pools for libvirt.")
        # To-Do: get names from configuration file
        commands = ["mkdir /data", "virsh pool-define-as hystck-pool dir - - - - /data/hystck-pool", "virsh pool-build hystck-pool", "virsh pool-start hystck-pool", "virsh pool-autostart hystck-pool"]
        for command in commands:
            prepCmd = command.format(line.strip())
            os.system(prepCmd)
        # Network Interface Setup
        logger.info("adding network interfaces.")
        # To-Do: get names from configuration file
        commands = ["virsh net-define public.xml", "virsh net-define private.xml", "virsh net-start public", "virsh net-start private", "virsh net-autostart public", "virsh net-autostart private"]
        for command in commands:
            prepCmd = command.format(line.strip())
            os.system(prepCmd)
    elif param == "vm":
        logger.info("nothing to do here.")
    else:
        logger.error("Unknown Parameter {}".format(param))
	
	

if __name__ == '__main__':
    main()
