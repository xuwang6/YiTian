#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : constants.py
# Author            : jason_wangxu@163.com
# Date              : 2024/5/18 12:17
# Last Modified     : 2024/5/18 12:17
# Description       : 常量
#
# Copyright (c) 2024, All rights reserved.
import os.path

PROJECT_ROOT = os.path.abspath("__file__").split("src")[0]

LOG_PATH = os.path.join(PROJECT_ROOT, "logs")
REPORT_PATH = os.path.join(PROJECT_ROOT, "reports")
RESOURCE_PATH = os.path.join(PROJECT_ROOT, "resources")
