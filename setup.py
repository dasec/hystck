#!/usr/bin/env python
# Copyright (C) 2013-2014 Reinhard Stampp
# Copyright (C) 2014-2016 Sascha Kopp
# This file is part of hystck - http://hystck.fbi.h-da.de
# See the file 'docs/LICENSE' for copying permission.
from distutils.core import setup

setup(
    name='hystck',
    version='1.0',
    packages=['hystck', 'hystck.attacks', 'hystck.botnet', 'hystck.botnet.net', 'hystck.botnet.net.meta', 'hystck.botnet.net.proto',
              'hystck.core', 'hystck.botnet.common', 'hystck.botnet.core', 'hystck.botnet.core.bmoncomponents',
              'hystck.utility', 'hystck.application', 'hystck.inputDevice', 'hystck.botnet.bots',
              'hystck.botnet.bots.hellobot', 'hystck.botnet.bots.mariposa', 'hystck.botnet.bots.zeus'],
    package_dir={'hystck': 'src/hystck'},
    package_data={'hystck': ['utility/conf/*']},
    url='hystck.fbi.h-da.de',
    license='',
    author='Reinhard Stampp, Sascha Kopp',
    author_email='reinhard.stampp@rstampp.net, sascha.kopp@stud.h-da.de',
    description='Python bindings for hystck.'
)
