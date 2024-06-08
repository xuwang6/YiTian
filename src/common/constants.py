#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : constants.py
# Author            : jason_wangxu@163.com
# Date              : 2024/5/18 12:17
# Last Modified     : 2024/5/18 12:17
# Description       : 常量
#
# Copyright (c) 2024, All rights reserved.
import json
import os.path

# 路径
PROJECT_ROOT = os.path.abspath(__file__).split("src")[0]
LOG_PATH = os.path.join(PROJECT_ROOT, "logs")
REPORT_PATH = os.path.join(PROJECT_ROOT, "reports")
RESOURCE_PATH = os.path.join(PROJECT_ROOT, "resources")

# 资源
LOCATOR_JSON = os.path.join(RESOURCE_PATH, "locator.json")
PACKAGES_JSON = os.path.join(RESOURCE_PATH, "packages.json")
with open(LOCATOR_JSON, "r", encoding="utf8") as f1, open(PACKAGES_JSON, "r", encoding="utf8") as f2:
    LOCATOR_DIC = json.load(f1)
    PACKAGES_DIC = json.load(f2)
