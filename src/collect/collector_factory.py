#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : collector_factory.py
# Author            : jason_wangxu@163.com
# Date              : 2024/6/8 15:06
# Last Modified     : 2024/6/8 15:06
# Description       :
#
# Copyright (c) 2024, All rights reserved.
from src.collect.cpu_collector import CpuCollector
from src.collect.fps_collector import FpsCollector
from src.collect.mem_collector import MemCollector


class CollectorFactory:
    """
    collector工厂类
    """

    def __init__(self, device, pkg, save, event):
        self.device = device
        self.pkg = pkg
        self.save = save
        self.event = event
        self.handler = None

    def begin_collect(self, name):
        """
        收集数据
        :param name:
        :return:
        """
        if name == "CPU":
            self.handler = CpuCollector(self.device, self.pkg, self.save, self.event)
        elif name == "MEM":
            self.handler = MemCollector(self.device, self.pkg[0], self.save, self.event)
        elif name == "FPS":
            self.handler = FpsCollector(self.device, self.pkg[0], self.save, self.event)
        else:
            self.handler = None
        self.handler.executor()

    def stop_collect(self):
        """
        停止收集
        """
        self.handler.terminate()
