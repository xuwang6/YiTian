#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : chrome_page.py
# Author            : jason_wangxu@163.com
# Date              : 2024/6/10 9:55
# Last Modified     : 2024/6/10 9:55
# Description       :
#
# Copyright (c) 2024, All rights reserved.
from src.pages.base_page import BasePage
from src.common import *


class TouTiaoPage(BasePage):
    def __init__(self):
        super(TouTiaoPage, self).__init__()
        self.pkg = [PACKAGES_DIC["今日头条"]]

    def search(self):
        pass
