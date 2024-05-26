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
import time

import uiautomator2 as u2
from src.common import *


class BasePage:
    def __init__(self):
        self.d = u2.connect(adb.devices[0])
        self._obj = None

    #
    # def _create_obj(self, locator: str):
    #     """
    #     创建元素对象
    #     :param locator:
    #     :return:
    #     """
    #     if locator.startswith("//"):
    #         return self.d.xpath(locator)
    #     else:
    #         dic = {}
    #         for item in locator.strip().split(","):
    #             key, value = item.split("=")
    #             dic[key] = value.strip('"')
    #         return self.d(**dic)

    @staticmethod
    def _create_obj(func):
        """
        创建元素对象
        :return:
        """

        def wrapper(self, *args, **kwargs):
            locator = LOCATOR_DIC[args[0].split("_")[0]][args[0]]
            print("元素对象：" + locator)
            if locator.startswith("//"):
                print("------>1")
                self._obj = self.d.xpath(locator)
            else:
                dic = {}
                for item in locator.strip().split(","):
                    key, value = item.split("=")
                    self._obj = value.strip('"')
                print("------>2")
                self._obj = self.d(**dic)
            return func(self, *args, **kwargs)

        return wrapper

    @_create_obj
    def wait_click(self, locator):
        """
        等待并点击
        :param locator:
        :return:
        """
        print(self._obj)
        # self._obj.click()
        self.d(text="应用").click()

    def open_app(self, package_name):
        """
        打开应用
        :param package_name:
        :return:
        """
        self.d.app_start(package_name)
        time.sleep(3)


if __name__ == "__main__":
    bp = BasePage()
    bp.open_app(PACKAGES_DIC["设置"])
    bp.wait_click("设置_BUTTON_应用")
