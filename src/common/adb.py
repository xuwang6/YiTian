#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @file name: adb.py
 @desc:
 @author: xu wang
 @mail: jason_wangxu@163.com
 @date: 2024/7/13 9:47
"""
from adbutils import adb
import re
import subprocess

from src.common.constants import RUN_CONFIG
from src.common.log import logger
from src.common.utils import read_yaml


class MyADB:
    def __init__(self):
        self.adb_env_status = False
        self.adb_connect_status = False
        if len(self.devices_list) == 0:
            logger.debug("未检测到adb设备，请人工确认！")
            exit()
        elif len(self.devices_list) == 1:
            self.device = self.devices_list[0]
        else:
            self.device = read_yaml(RUN_CONFIG)["device"]
        self.d = adb.device(self.device)
        self.os_type = ""

    def check_adb_env(self):
        """
        check adb env
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
        get devices list
        :return:
        """
        d_list = []
        if self.check_adb_env():
            for item in adb.device_list():
                d_list.append(item.serial)
        else:
            logger.debug("adb环境异常！")
        logger.debug("设备列表：" + str(d_list))
        return d_list

    @staticmethod
    def connect(ip_device, timeout):
        """
        adb connect device
        ip_device: ip address
        timeout: timeout
        :return:
        """
        return adb.connect(ip_device, timeout=timeout)

    @staticmethod
    def disconnect(ip_device):
        """
        adb disconnect device
        ip_device: ip address
        timeout: timeout
        :return:
        """
        return adb.disconnect(ip_device)

    @staticmethod
    def adb_wait_connect(name, timeout):
        """
        wait adb connect device
        name: device name
        timeout: timeout
        """
        adb.wait_for(name, state="device", timeout=timeout)

    @staticmethod
    def adb_wait_disconnect(name, timeout):
        """
        wait adb disconnect device
        name: device name
        timeout: timeout
        """
        adb.wait_for(name, state="disconnect", timeout=timeout)

    def adb_root(self):
        """
        adb root
        """
        self.d.root()

    def adb_reboot(self):
        """
        adb reboot
        """
        self.d.reboot()

    def adb_shell_command(self, cmd, *args, **kwargs):
        """
        adb shell
        """
        return self.d.shell(cmd, *args, **kwargs)

    def adb_logcat_save(self, name, clear=True, timeout=60):
        """
        adb logcat file
        name: file name
        clear: clear before logcat
        timeout: timeout
        """
        logcat = self.d.logcat(name, clear=clear)
        logcat.stop(timeout=timeout)

    def adb_logcat_filter(self, name, clear=True, filter_str=None, timeout=60):
        """
        adb logcat file
        name: file name
        clear: clear before logcat
        filter_str: filter value
        timeout: timeout
        """
        logcat = self.d.logcat(file=name, clear=clear, re_filter=filter_str)
        logcat.stop(timeout=timeout)

    @property
    def cpu_core_num(self):
        """
        get cpu core number by top
        因为发现通过/proc/cpuinfo获取获取的核数量和top的不一致（部分手机，例如IQOO Z5），故未使用此方法
        """
        re_cpu = re.compile(
            r'(\d+)\%cpu\s+(\d+)\%user\s+(\d+)\%nice\s+(\d+)\%sys\s+(\d+)\%idle\s+(\d+)\%iow\s+(\d+)\%irq\s+('
            r'\d+)\%sirq\s+(\d+)\%host')
        r = self.adb_shell_command("top -n 1")
        try:
            for line in r.split("\n"):
                if re_cpu.search(line):
                    logger.debug(line)
                    return line.strip()[0]
        except Exception as e:
            print(e)


if __name__ == "__main__":
    my_adb = MyADB()
    count = my_adb.cpu_core_num
    print(count)
