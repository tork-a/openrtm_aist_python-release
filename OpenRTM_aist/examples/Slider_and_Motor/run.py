#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

#
# @file run.py
# @brief ExtTrigger example startup script
# @date $Date: 2007/10/26 $
#
# Copyright (c) 2003-2007 Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#          Task-intelligence Research Group,
#          Intelligent System Research Institute,
#          National Institute of Industrial Science (AIST), Japan
#          All rights reserved.
#

import sys,os,platform
import time
import subprocess

nsport="2809"
sysinfo = platform.uname()
hostname= sysinfo[1]
plat=sys.platform

if plat == "win32":
    os.system("start python ..\\..\\..\\bin\\rtm-naming.py")
    os.system("start python SliderComp.py")
    os.system("start python TkMotorComp.py")
    time.sleep(2)
    os.system("python Connector.py")

else:
    status,term=subprocess.getstatusoutput("which xterm")
    term += " -e"
    if status != 0:
        status,term=subprocess.getstatusoutput("which kterm")
        term += " -e"

    if status != 0:
        status,term=subprocess.getstatusoutput("which uxterm")
        term += " -e"

    if status != 0:
        status,term=subprocess.getstatusoutput("which gnome-terminal")
        term += " -x"

    if status != 0:
        print("No terminal program (kterm/xterm/gnome-terminal) exists.")
        exit

    path = None
    for p in sys.path:
        if os.path.exists(os.path.join(p,"OpenRTM_aist")):
            path = os.path.join(p,"OpenRTM_aist","utils","rtm-naming")
            break
    if path is None:
        print("rtm-naming directory not exist.")
        sys.exit(0)

    os.system('python %s/rtm-naming.py &'%path)
    os.system('%s python SliderComp.py &'%term)
    os.system('%s python TkMotorComp.py &'%term)
    time.sleep(3)
    os.system("python Connector.py")
