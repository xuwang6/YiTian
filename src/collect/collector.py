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


class Collector(metaclass=ABCMeta):
    """
    collector抽象类
    """

    def __init__(self, *arg, **kwargs):
        pass

    @abstractmethod
    def executor(self):
        pass

    @abstractmethod
    def terminate(self):
        pass

#
# class Collector(ABCMeta):
#     def __init__(self, device, core, pkg, save, event):
#         super().__init__()
#         self.device = device
#         self.core = core
#         self.pkg = pkg
#         self.save = save
#         self.event = event
#
#     @abstractmethod
#     def executor(self):
#         pass
#
#     @abstractmethod
#     def terminate(self):
#         pass
