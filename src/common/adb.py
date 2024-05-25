#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : adb.py
# Author            : jason_wangxu@163.com
# Date              : 2024/5/18 10:58
# Last Modified     : 2024/5/18 10:58
# Description       :
#
# Copyright (c) 2024, All rights reserved.
import subprocess
from src.common.log import log


class ADB:
    def __init__(self):
        self.adb_env_status = False
        self.adb_connect_status = False
        self.devices = self.devices_list()
        self.os_type = ""

    def check_adb_env(self):
        """
        检查adb是否配置环境变量
        :return:
        """
        try:
            r = subprocess.run(["adb", "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if r.returncode == 0:
                self.adb_env_status = True
                log.debug("adb环境变量已配置：\n" + r.stdout)
            else:
                log.debug("adb未配置环境变量！")
        except Exception as e:
            log.debug(e)
        return self.adb_env_status

    def devices_list(self):
        """
        获取adb 设备
        :return:
        """
        d_list = []
        if self.check_adb_env():
            r = subprocess.Popen(["adb", "devices"], encoding="utf8", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for line in r.stdout.readlines():
                line = line.strip()
                if line.endswith("device"):
                    d_list.append(line.split("\t")[0])
            if len(d_list) < 1:
                log.debug("当前未检测到adb设备， 请人工确认！")
                exit()
        else:
            log.debug("adb环境异常！")
        log.debug("设备列表：" + str(d_list))
        return d_list

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
