#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : adb.py
# Author            : jason_wangxu@163.com
# Date              : 2024/5/18 10:58
# Last Modified     : 2024/5/18 10:58
# Description       :
#
# Copyright (c) 2024, All rights reserved.
import re
import subprocess

from src.common.constants import RUN_CONFIG
from src.common.log import logger
from src.common.utils import read_yaml


class ADB:
    def __init__(self):
        self.adb_env_status = False
        self.adb_connect_status = False
        if len(self.devices_list) > 1:
            self.device = read_yaml(RUN_CONFIG)["device"]
        else:
            self.device = self.devices_list[0]
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
                logger.debug("adb环境变量已配置：\n" + r.stdout)
            else:
                logger.debug("adb未配置环境变量！")
        except Exception as e:
            logger.debug(e)
        return self.adb_env_status

    @property
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
                logger.debug("当前未检测到adb设备， 请人工确认！")
                exit()
        else:
            logger.debug("adb环境异常！")
        logger.debug("设备列表：" + str(d_list))
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

    def adb_shell_command(self, cmd, *args, **kwargs):
        """
        adb shell
        """
        cmd_list = ["adb", "-s", self.device, "shell", cmd]
        for item in args:
            cmd_list.append(item)
        cmd_str = " ".join(cmd_list)
        r = subprocess.Popen(cmd_str, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             shell=True, encoding="utf8", )
        (out, error) = r.communicate()
        if out == '':
            out = error
        return out

    def adb_logcat(self):
        pass

    @property
    def cpu_core_num(self):
        """
        通过top获取cpu核数
        因为发现通过/proc/cpuinfo获取获取的核数量和top的不一致（部分手机，例如IQOO Z5），故未使用此方法
        """
        re_cpu = re.compile(
            r'(\d+)\%cpu\s+(\d+)\%user\s+(\d+)\%nice\s+(\d+)\%sys\s+(\d+)\%idle\s+(\d+)\%iow\s+(\d+)\%irq\s+('
            r'\d+)\%sirq\s+(\d+)\%host')
        r = self.adb_shell_command("top")
        try:
            for line in r.split("\n"):
                if re_cpu.search(line):
                    return line.strip()[0]
        except Exception as e:
            print(e)


if __name__ == "__main__":
    adb = ADB()
    count = adb.get_pid("com.android.chrome")
    print(count)
