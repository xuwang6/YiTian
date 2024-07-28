#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : writer.py
# Author            : jason_wangxu@163.com
# Date              : 2024/6/8 14:21
# Last Modified     : 2024/6/8 14:21
# Description       :
#
# Copyright (c) 2024, All rights reserved.
import os.path
from abc import ABCMeta, abstractmethod


class Writer(metaclass=ABCMeta):
    """
    writer抽象类
    """

    def __init___(self, *args, **kwargs):
        pass

    @abstractmethod
    def generate(self):
        pass

    @abstractmethod
    def _write_excel(self, name):
        """
        数据写入excel文件
        :return:
        """
        pass

    @abstractmethod
    def _write_csv(self, name):
        """
        写csv文件
        """
        pass

    @staticmethod
    def _read_csv(name):
        """
        读取csv文件
        """
        lines = []
        with open(os.path.join(name), encoding="utf8", mode="r") as f:
            for line in f:
                lines.append(line.split(","))
        return lines
