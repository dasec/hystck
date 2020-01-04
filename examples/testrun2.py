#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import platform
import time
import logging
import subprocess

try:
    from hystck.core.vmm import Vmm
    from hystck.utility.logger_helper import create_logger
    from hystck.core.vmm import GuestListener

except ImportError as e:
    print("Import error in hystckmaster.py! " + str(e))
    sys.exit(1)


def create_vm(logger):
    # virtual_machine_monitor1 = Vmm(logger, linux_template='linux_template')
    macsInUse = []
    guests = []
    guestListener = GuestListener(guests, logger)
    virtual_machine_monitor1 = Vmm(macsInUse, guests, logger)
    #guest = virtual_machine_monitor1.create_guest(guest_name="l-guest01", platform="linux", boottime=None)
    guest = virtual_machine_monitor1.create_guest(guest_name="w-guest01", platform="windows", boottime=None)
    logger.debug("Try connecting to guest")

    while guest.state != "connected":
        logger.debug(".")
        time.sleep(1)

    logger.debug(guest.guestname + " is connected!")

    return guest


def main():
    """
    Test Script for hystck.

    :return: no return value
    """
    try:
        logger = create_logger('hystckManager', logging.DEBUG)
        logger.info("This is a test script to check the functionallity of the hystck library" + '\n')

        guest = create_vm(logger)

        # call all test functions you want to run
        tests = {'firefox': test_firefox, 'thunderbird': test_thunderbird} # all available test functions
        arguments = sys.argv[1:] # every argument but the first as the first is the filename

        for argument in arguments:
            try:
                tests[argument](guest, logger)
            except Exception as e:
                print("argument unknown: " + str(e))

        time.sleep(5)
        guest.remove("keep")

    ######## CLEANUP ############# ERROR HANDLING
    except KeyboardInterrupt as k:
        logger.debug(k)
        logger.debug("KeyboardInterrupt")
        logger.debug(k)
        logger.debug(virtual_machine_monitor1)
        raw_input("Press Enter to continue...")
        virtual_machine_monitor1.clear()
        logger.debug("cleanup here")
        try:
            virtual_machine_monitor1.clear()
        except NameError:
            logger.debug("well, host1 was not defined!")

        exit(0)

    except Exception as e:
        logger.debug("main gets the error: " + str(e))
        logger.debug("cleanup here")
        raw_input("Press Enter to continue...")
        try:
            virtual_machine_monitor1.clear()
            subprocess.call(["/etc/init.d/libvirt-bin", "restart"])
        except NameError:
            logger.debug("well, host1 was not defined!")
        sys.exit(1)


def test_firefox(guest, logger):
    logger.debug("test_firefox() started.")
    browser_obj = None
    browser_obj = guest.application("webBrowserFirefox", {'webBrowser': "firefox"})
    # open browser with blank page
    browser_obj.open(url="dasec.fbi.h-da.de")
    while browser_obj.is_busy:
        time.sleep(2)
    # browse sites
    browser_obj.browse_to("heise.de")
    while browser_obj.is_busy:
        time.sleep(5)
    time.sleep(10)
    # facebook login
    browser_obj.browse_to("facebook.com")
    while browser_obj.is_busy:
        time.sleep(5)
    browser_obj.facebook_login("tom-g1@gmx.de", "FBgoeshystck", "loginbutton")
    time.sleep(25)
    # download file
    browser_obj.browse_to("python.org/downloads")
    while browser_obj.is_busy:
        time.sleep(15)
    browser_obj.click_xpath_test('/html/body/div/div[3]/div/section/div[1]/ol/li[1]/span[3]/a')
    time.sleep(25)
    browser_obj.click_xpath_test('/html/body/div/div[3]/div/section/article/table/tbody/tr[1]/td[1]/a')
    time.sleep(25)
    browser_obj.press_enter_test()
    time.sleep(25)

    # close browser
    browser_obj.close()
    while browser_obj.is_busy:
        time.sleep(5)
    logger.debug("test_firefox() ended.")

def test_thunderbird(guest, logger):
    logger.debug("test_thunderbird() started.")
    mail = guest.application("mailClientThunderbird", {})

    if platform.system() == "Windows": # need to open once before in Windows to work properly, but in Linux this produces an error.
        mail.open()
        while mail.is_busy:
            time.sleep(2)
        time.sleep(60)
        mail.close()
        while mail.is_busy:
            time.sleep(2)
        time.sleep(20)

    # Important set a password used by the mail service, it will be saved inside thunderbird
    mail.set_session_password("newPass2019")
    while mail.is_busy:
        time.sleep(1)

    time.sleep(20)
    # Prepare a new Profile; assume the profile folders don't exist; these options assume a insecure mail server without SSL/TLS using an unencrypted password exchange
    # theo.11111@web.de / hystckMail / Theo Tester
    mail.add_imap_account("imap.web.de", "smtp.web.de", "theo.test1@web.de", "theo.test1", "Theo Tester", "Example", 2,
                          3, 1, 3)
    while mail.is_busy:
        time.sleep(1)
    time.sleep(20)
    # Open thunderbird and check for mail
    mail.open()
    while mail.is_busy:
        time.sleep(1)
    time.sleep(60)
    # We are done close the application
    mail.close()
    while mail.is_busy:
        time.sleep(1)
    time.sleep(10)
    # Send a new mail by invoking thunderbird with special command line options
    mail.send_mail(message="testmail", subject="testmail", receiver="thomas.schaefer91@gmx.de")
    while mail.is_busy:
        time.sleep(1)
    time.sleep(20)
    logger.debug("test_thunderbird() ended.")

if __name__ == "__main__":
    try:
        main()
    except:
        sys.exit(1)
