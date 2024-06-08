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
    def __init__(self, device, core, pkg, save, event):
        self.device = device
        self.core = core
        self.pkg = pkg
        self.save = save
        self.event = event

    def collect_data(self, name):
        """
        收集数据
        :param name:
        :return:
        """
        if name == "CPU":
            cpu = CpuCollector(self.device, self.core, self.pkg, self.save, self.event)
            cpu.executor()
        elif name == "MEM":
            mem = MemCollector(self.device, self.pkg, self.save, self.event)
            mem.executor()
        elif name == "FPS":
            fps = FpsCollector(self.device, self.pkg, self.save, self.event)
            fps.executor()
