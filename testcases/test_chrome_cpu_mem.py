#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : test_chrome_cpu_mem.py
# Author            : jason_wangxu@163.com
# Date              : 2024/5/18 11:54
# Last Modified     : 2024/5/18 11:54
# Description       :
#
# Copyright (c) 2024, All rights reserved.
import pytest

from src.pages.chrome_page import ChromePage
from src.common import *

page = ChromePage()


@pytest.mark.parametrize("init_class", page.pkg, indirect=True)
class TestCase:
    def test_chrome_cpu_mem_search(self):
        page.close_app(page.pkg)
        page.open_app(page.pkg)
        logger.info("点击输入框...")
        page.wait_click("Chrome_EDIT_搜索框")
        page.input_text("www.baidu.com", clear=True, enter=True)


if __name__ == "__main__":
    pytest.main(["-vs", "test_chrome_cpu_mem.py"])
