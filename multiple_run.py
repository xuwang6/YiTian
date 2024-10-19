#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @file name: multiple_run.py.py
 @desc:
 @author: xu wang
 @mail: jason_wangxu@163.com
 @date: 2024/9/6 21:19
"""
import subprocess
import threading
import time

from src.common import RUN_CONFIG, modify_yaml


def execute():
    subprocess.run("python run.py")


devices_list = ["emulator-5554", "emulator-5556"]
for item in devices_list:
    modify_yaml(RUN_CONFIG, "device", item)
    threading.Thread(target=execute, daemon=False).start()
    time.sleep(2)
