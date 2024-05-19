#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : base_page.py
# Author            : jason_wangxu@163.com
# Date              : 2024/5/18 10:33
# Last Modified     : 2024/5/18 10:33
# Description       :
#
# Copyright (c) 2024, All rights reserved.


import uiautomator2 as u2
from src.common import *


class BasePage:
    def __init__(self):
        self.d = u2.connect(adb.device_list)



