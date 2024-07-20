#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @file name: demo.py
 @desc:
 @author: xu wang
 @mail: jason_wangxu@163.com
 @date: 2024/6/22 17:27
"""

import xlsxwriter
from numpy import mean

from src.write.cpu_writer import CpuWriter
from src.write.fps_writer import FpsWriter
from src.write.mem_writer import MemWriter


class WriterFactory:
    def __init__(self, pkg, save, data):
        self.pkg = pkg
        self.save = save
        self.data = data
        self.handler = None

    def write_data(self, name):
        """
        写数据
        :param name:
        :return:
        """
        if name == "CPU":
            print("----------------00---------------", self.pkg, self.save, self.data)
            self.handler = CpuWriter(self.pkg, self.save, self.data)
            print("----------------01---------------", self.pkg, self.save, self.data)
        elif name == "MEM":
            self.handler = MemWriter(self.pkg, self.save, self.data)
        elif name == "FPS":
            self.handler = FpsWriter(self.pkg, self.save, self.data)
        else:
            self.handler = None
        print("----------------02---------------", self.pkg, self.save, self.data)
        self.handler.generate()

    def terminate(self):
        """
        停止
        """
        self.handler._stop = True
