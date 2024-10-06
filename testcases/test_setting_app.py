#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : test_chrome_cpu_mem.py
# Author            : jason_wangxu@163.com
# Date              : 2024/5/18 11:54
# Last Modified     : 2024/5/18 11:54
# Description       :
#
# Copyright (c) 2024, All rights reserved.
import random
import time

import pytest

from src.pages.setting_page import SettingPage
from src.common import *

page = SettingPage()


class TestCase:
    @pytest.mark.smt
    @pytest.mark.parametrize("init_case", [page.pkg], indirect=True)
    def test_setting_app(self, init_case):
        page.close_app(page.pkg)
        page.open_app(page.pkg)
        init_case.set()
        for index in range(50):
            logger.info(f"这是第{index + 1}轮...")
            page.ele_wait_swipe("设置_VIEW_主页", random.choice(["up", "down"]))


if __name__ == "__main__":
    pytest.main(["-vs", "test_setting_app.py"])
