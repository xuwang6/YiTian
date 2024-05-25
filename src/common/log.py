#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : log.py
# Author            : jason_wangxu@163.com
# Date              : 2024/5/18 11:12
# Last Modified     : 2024/5/18 11:12
# Description       :
#
# Copyright (c) 2024, All rights reserved.

import logging
import os.path
import sys
import time
from src.common.constants import LOG_PATH


class Logger:
    def __init__(self, name, log_file, level='DEBUG'):
        # 创建一个logger
        self.logger = logging.getLogger(name)
        self.log_file = log_file
        self.level = level
        self.encoding = sys.stdout.encoding

        # 设置日志级别
        if level.upper() == 'INFO':
            self.logger.setLevel(logging.INFO)
        elif level.upper() == 'DEBUG':
            self.logger.setLevel(logging.DEBUG)
        elif level.upper() == 'ERROR':
            self.logger.setLevel(logging.ERROR)
        elif level.upper() == 'WARNING':
            self.logger.setLevel(logging.WARNING)
        elif level.upper() == 'CRITICAL':
            self.logger.setLevel(logging.CRITICAL)

        # 创建一个handler，用于写入日志文件
        time_stamp = time.strftime("%y%m%d-%H%M%S", time.localtime())
        f_handler = logging.FileHandler(os.path.join(log_file, f"{time_stamp}.log"))
        f_handler.setLevel(self.logger.level)
        f_handler.encoding = self.encoding

        # 创建一个handler，用于将日志输出到控制台
        s_handler = logging.StreamHandler(sys.stdout)
        s_handler.setLevel(self.logger.level)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(formatter)
        s_handler.setFormatter(formatter)

        self.logger.addHandler(f_handler)
        self.logger.addHandler(s_handler)

    def get_logger(self):
        return self.logger


log = Logger("YiTian", LOG_PATH).get_logger()
