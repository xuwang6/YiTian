#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : utils.py
# Author            : jason_wangxu@163.com
# Date              : 2024/5/25 17:11
# Last Modified     : 2024/5/25 17:11
# Description       :
#
# Copyright (c) 2024, All rights reserved.
import os
import time


def timestamp_ymd():
    """
    format timestamp
    :return: 240609
    """
    timestamp = time.strftime("%y%m%d", time.localtime())
    return timestamp


def timestamp_ymd_hms():
    """
    format timestamp
    :return: 240609_133057
    """
    timestamp = time.strftime("%y%m%d_%H%M%S", time.localtime())
    return timestamp


def create_folder(path):
    """
    create folder
    :param path:
    :return:
    """
    os.makedirs(path, exist_ok=True)
