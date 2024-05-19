#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : adb.py
# Author            : jason_wangxu@163.com
# Date              : 2024/5/18 10:58
# Last Modified     : 2024/5/18 10:58
# Description       :
#
# Copyright (c) 2024, All rights reserved.
import os
import subprocess
from src.common import *


class ADB:
    def __init__(self):
        self.adb_exist = False
        self.device_list = []
        self.os_type = ""

    def check_adb_env(self):
        """
        检查adb是否配置环境变量
        :return:
        """
        try:
            r = subprocess.run(["adb", "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if r.returncode == 0:
                self.adb_exist = True
                log.debug("adb环境变量已配置：\n" + r.stdout)
            else:
                log.debug("adb未配置环境变量！")
        except Exception as e:
            log.debug(e)
        return self.adb_exist

    def list_devices(self):
        """
        获取adb 设备
        :return:
        """
        if self.check_adb_env():
            r = subprocess.Popen(["adb", "devices"], encoding="utf8", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for line in r.stdout.readlines():
                line = line.strip()
                if line.endswith("device"):
                    self.device_list.append(line.split("\t")[0])
        else:
            log.debug("adb环境异常！")
        log.debug("设备列表：" + str(self.device_list))
        return self.device_list

    @staticmethod
    def connect(ip_device):
        """
        adb链接device
        :return:
        """
        r = subprocess.run(["adb", "connect", ip_device], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           text=True)
        return r.stdout

    def disconnect(self):
        pass

    def adb_command(self):
        pass

    def adb_shell_command(self):
        pass

    def adb_logcat(self):
        pass


if __name__ == "__main__":
    adb = ADB()
    adb.list_devices()
