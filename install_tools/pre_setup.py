#!/usr/bin/python3
#test
import sys
import os
import logging
import json
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
    # Check Command Line parameter, if none is given set to "vm"
    if len(sys.argv) >= 2:
        param = sys.argv[1]
    else:
        param = "vm"

    # Load config file and read different sections into variables
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
        general = data['general']
        tcpdump = data['tcpdump']
        virtpools = data['libvirt-pools']
        netifaces = data['network-interfaces']
    
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

    # Check if installation is host or vm side
    if param == "host":
        # Add Usergroup libvirtd
        os.system("groupadd libvirtd")
        os.system("usermod -a -G libvirtd {}".format(general['user']))

        # Setup tcpdump user rights
        logger.info("setting up tcpdump.")
        os.system("setcap cap_net_raw,cap_net_admin=eip {}".format(tcpdump['path']))

        # Add Pools for Libvirt
        logger.info("adding pools for libvirt.")
        # To-Do: get names from configuration file
        commands = ["mkdir {}".format(data['libvirt-pools']['path']),
                    "virsh pool-define-as hystck-pool dir - - - - {}/{}".format(virtpools['path'], virtpools['name']),
                    "virsh pool-build {}".format(virtpools['name']),
                    "virsh pool-start {}".format(virtpools['name']),
                    "virsh pool-autostart {}".format(virtpools['name'])]
        for command in commands:
            prepCmd = command.format(line.strip())
            os.system(prepCmd)

        # Network Interface Setup
        logger.info("adding network interfaces.")
        # To-Do: get names from configuration file
        commands = ["virsh net-define {}".format(netifaces['public-interface-config-file']),
                    "virsh net-define {}".format(netifaces['private-interface-config-file']),
                    "virsh net-start {}".format(netifaces['public-interface-name']),
                    "virsh net-start {}".format(netifaces['private-interface-name']),
                    "virsh net-autostart {}".format(netifaces['public-interface-name']),
                    "virsh net-autostart {}".format(netifaces['private-interface-name'])]
        for command in commands:
            prepCmd = command.format(line.strip())
            os.system(prepCmd)

        # Reboot to enable virt-manager user privileges
        os.system("reboot")
    elif param == "vm":
        logger.info("nothing to do here.")
    else:
        logger.error("Unknown Parameter {}".format(param))
	
	

if __name__ == '__main__':
    main()
