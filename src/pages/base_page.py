#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : base_page.py
# Author            : jason_wangxu@163.com
# Date              : 2024/5/18 10:33
# Last Modified     : 2024/5/18 10:33
# Description       :
#
# Copyright (c) 2024, All rights reserved.
import json
import os.path

import uiautomator2 as u2
from src.common import *


class BasePage:
    def __init__(self):
        self.d = u2.connect(adb.devices[0])
        self.json = "locator.json"

    def _create_obj(self, locator: str):
        """
        创建元素对象
        :param locator:
        :return:
        """
        if locator.startswith("//"):
            return self.d.xpath(locator)
        else:
            dic = {}
            for item in locator.strip().split(","):
                key, value = item.split("=")
                dic[key] = value.strip('"')
            return self.d(**dic)

    def parse_locator(self, locator):
        """
        load locator.json
        :return:
        """
        args = locator.split("_")
        with open(os.path.join(constants.RESOURCE_PATH, self.json), encoding="utf8") as f:
            content = json.load(f)
        print(content)

    def wait_click(self, locator):
        pass


if __name__ == "__main__":
    bp = BasePage()
    bp.parse_locator("设置_BUTTON_个性化")
