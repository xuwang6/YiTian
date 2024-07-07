#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : collector.py
# Author            : jason_wangxu@163.com
# Date              : 2024/6/8 14:34
# Last Modified     : 2024/6/8 14:34
# Description       :
#
# Copyright (c) 2024, All rights reserved.
from abc import ABCMeta, abstractmethod
from src.common import *


class Collector(metaclass=ABCMeta):
    """
    collector抽象类
    """

    def __init___(self, *args, **kwargs):
        pass

    @abstractmethod
    def executor(self):
        pass

    @abstractmethod
    def terminate(self):
        pass

    @staticmethod
    def _get_pid(pkg):
        return adb.adb_shell_command("pidof %s" % pkg)
