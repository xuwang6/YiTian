#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : mem_collector.py
# Author            : jason_wangxu@163.com
# Date              : 2024/6/8 14:37
# Last Modified     : 2024/6/8 14:37
# Description       :
#
# Copyright (c) 2024, All rights reserved.

import os
import queue
import re
import threading
import time

from src.collect.collector import Collector
from src.common import utils
from src.common.log import logger
from src.write.writer_factory import WriteFactory


class MemCollector(Collector):
    def __init__(self, device, pkg, save, event):
        super().__init__(device, pkg, save, event)
        self._stop = False
        self.device = device
        self.pkg = pkg
        self.head = ['时间', 'CPU', '内存']
        self.dur = 1.0

    def executor(self):
        self.event.wait()
        q2 = queue.Queue()
        factory = WriteFactory("MEM", self.pkg, self.save, q2)
        t = threading.Thread(target=factory.generate)
        t.start()
        with open(os.path.join(self.save, "dumpsys_meminfo_%s.log" % self.pkg.replace(":", "-")),
                  mode="w") as meminfo, open(os.path.join(self.save, "free.log"), mode="w") as free:
            while True:
                begin = time.time()
                if self._stop:
                    q2.put("over")
                    break
                info = []
                cur = utils.get_time_yr_sfmms()
                info.append(cur)
                mem_info = os.popen(f"adb -s {self.device} shell free -h")
                for line in mem_info.readlines():
                    free.write(line)
                    if "Mem:" in line:
                        line = re.sub(r"\s+", " ", line).strip()
                        logger.debug("Mem<---%s" % line)
                        tmp = line.split(" ")
                        info.append(tmp[1])
                        info.append(tmp[2])
                        info.append(tmp[3])
                pid = self._get_pid(self.pkg)
                if pid == 0:
                    logger.debug(f"未发现应用{self.pkg}，请确认是否正常运行！！")
                    return
                mem_info = os.popen(f'''adb -s {self.device} shell "dumpsys meminfo --local -s {pid}"''')
                logger.debug(f'''adb -s {self.device} shell "dumpsys meminfo --local -s {pid}"''')
                info.append(pid)
                for line in mem_info.readlines():
                    meminfo.write(line)
                    if "Java Heap:" in line:
                        logger.debug("Java Heap<---%s" % line)
                        info.append(float(re.findall(r"(\d+)", line)[0]) / 1000)
                    if "Native Heap:" in line:
                        logger.debug("Native Heap<---%s" % line)
                        info.append(float(re.findall(r"(\d+)", line)[0]) / 1000)
                    if "TOTAL SWAP" in line:
                        logger.debug("TOTAL PSS<--- %s" % line)
                        info.append(float(re.findall(r"(\d+)", line)[0]) / 1000)
                logger.info(f"Time/Total/Used/Free/PID/PID_JavaHeap/PID_NativeHeap/PID_PSS：{info}")
                q2.put(info)
                cost = time.time() - begin
                logger.debug("耗时：%f" % cost)
                if self.dur > cost:
                    time.sleep(self.dur - cost)

    def terminate(self):
        self._stop = True
