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
            logger.debug("元素对象：" + locator)
            if locator.startswith("//"):
                logger.debug("------>xpath")
                self._obj = self.d.xpath(locator)
            else:
                dic = {}
                for item in locator.strip().split(","):
                    key, value = item.split("=")
                    self._obj = value.strip('"')
                logger.debug("------>element")
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
        self._obj.wait(timeout=10)
        self._obj.click()

    def open_app(self, package_name):
        """
        打开应用
        :param package_name:
        :return:
        """
        if isinstance(package_name, list):
            for item in package_name:
                self.d.app_start(item)
        else:
            self.d.app_start(package_name)
        time.sleep(3)

    def close_app(self, package_name):
        """
        关闭应用
        :param package_name:
        :return:
        """
        if isinstance(package_name, list):
            for item in package_name:
                self.d.app_stop(item)
        else:
            self.d.app_stop(package_name)
        time.sleep(1)

    def input_text(self, text: str, clear=False, enter=True):
        """
        输入文字
        :param enter:
        :param clear:
        :param text:
        :return:
        """
        self.d.send_keys(text, clear)
        time.sleep(1)
        if enter:
            self.d.press("enter")

    def cpu_core_num(self):
        """
        获取CPU核心数
        :return:
        """
        return self.d.shell("cat /proc/cpuinfo | grep 'processor' | wc -l")


if __name__ == "__main__":
    bp = BasePage()
    bp.close_app(PACKAGES_DIC["Chrome"])
    bp.open_app(PACKAGES_DIC["Chrome"])
    bp.wait_click("Chrome_EDIT_搜索框")
    bp.input_text("www.baidu.com", clear=True, enter=True)
