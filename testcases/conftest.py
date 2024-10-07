#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : conftest.py
# Author            : jason_wangxu@163.com
# Date              : 2024/6/8 16:20
# Last Modified     : 2024/6/8 16:20
# Description       :
#
# Copyright (c) 2024, All rights reserved.
import threading

import pytest

from src.collect.collector_factory import CollectorFactory
from src.common import *


@pytest.fixture(scope="session", autouse=True)
def init_session():
    logger.debug("init_session begin!")
    yield
    logger.debug("init_session end!")


@pytest.fixture(scope="class", autouse=True)
def init_class(request):
    logger.debug("init_class begin!")
    yield
    logger.debug("init_class end!")


@pytest.fixture(scope="function", autouse=True)
def init_case(request):
    event = threading.Event()
    logger.debug(f"=>{request.function.__name__}")
    report_folder = os.path.join(REPORT_PATH, "%s_%s" % (request.function.__name__, timestamp_ymd_hms()))
    create_folder(report_folder)
    cpu = CollectorFactory(adb.device, request.param, report_folder, event)
    threading.Thread(target=cpu.begin_collect, args=["CPU"]).start()
    mem_threads = []
    fps_threads = []
    if type(request.param) is list:
        for item in request.param:
            mem_item = CollectorFactory(adb.device, item, report_folder, event)
            fps_item = CollectorFactory(adb.device, item, report_folder, event)
            threading.Thread(target=mem_item.begin_collect, args=["MEM"]).start()
            threading.Thread(target=fps_item.begin_collect, args=["FPS"]).start()
            mem_threads.append(mem_item)
            fps_threads.append(fps_item)
    else:
        mem = CollectorFactory(adb.device, request.param, report_folder, event)
        fps = CollectorFactory(adb.device, request.param, report_folder, event)
        threading.Thread(target=mem.begin_collect, args=["MEM"]).start()
        threading.Thread(target=fps.begin_collect, args=["FPS"]).start()
        mem_threads.append(mem)
        fps_threads.append(fps)
    yield event
    cpu.stop_collect()
    for item in mem_threads:
        item.stop_collect()
    for item in fps_threads:
        item.stop_collect()
    print("case over!")
