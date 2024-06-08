#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : test_demo.py
# Author            : jason_wangxu@163.com
# Date              : 2024/5/18 11:54
# Last Modified     : 2024/5/18 11:54
# Description       :
#
# Copyright (c) 2024, All rights reserved.
import pytest

from src.pages.base_page import BasePage
from src.common import *

bp = BasePage()


class TestCase:
    def test_demo(self):
        bp.close_app(PACKAGES_DIC["Chrome"])
        bp.open_app(PACKAGES_DIC["Chrome"])
        bp.wait_click("Chrome_EDIT_搜索框")
        bp.input_text("www.baidu.com", clear=True, enter=True)


if __name__ == "__main__":
    pytest.main(["-vs"])
