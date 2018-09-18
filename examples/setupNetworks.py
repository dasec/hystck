#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Reinhard Stampp
# This file is part of hystck - http://hystck.fbi.h-da.de
# See the file 'docs/LICENSE' for copying permission.

"""This python script create and start the networks local and internet using libvirt.

"""
import sys


try:
    from hystck.utility.network import setup_networks
    from hystck.utility.network import stop_and_delete_networks

except ImportError as e:
    print("Import error in main.py! " +str(e))


def main():
    setup_networks()


if __name__ == "__main__":
    try:
        main()
    except:
        sys.exit(1)
