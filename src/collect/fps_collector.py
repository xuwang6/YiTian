#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : fps_collector.py
# Author            : jason_wangxu@163.com
# Date              : 2024/6/8 14:37
# Last Modified     : 2024/6/8 14:37
# Description       :
#
# Copyright (c) 2024, All rights reserved.

import queue
import threading

from src.collect.collector import Collector
from src.common import *
from src.common.log import logger
from src.write.writer_factory import WriterFactory


class FpsCollector(Collector):
    def __init__(self, device, pkg, save, event, freq=1):
        super().__init__()
        self.device = device
        self.pkg = pkg
        self.save = save
        self.event = event
        self._stop = False
        self.refresh_rate = 0
        self.nanoseconds_per_second = 1e9
        self.freq = freq

    def executor(self) -> None:
        os.popen("adb -s %s shell dumpsys gfxinfo %s reset" % (self.device, self.pkg))
        self.event.wait()
        q = queue.Queue()
        factory = WriterFactory("FPS", self.pkg, self.save, q)
        t = threading.Thread(target=factory.write_data, args="FPS")
        t.start()
        with open(os.path.join(self.save, "dumpsys_gfxinfo_%s.log" % self.pkg.replace(":", "-")),
                  mode="w") as gfxinfo:
            if self.refresh_rate == 0:
                try:
                    r = os.popen("adb -s %s shell dumpsys SurfaceFlinger --latency" % self.device)
                    self.refresh_rate = float(r.readline().strip()) / self.nanoseconds_per_second  # 毫秒
                    logger.info("屏幕刷新率时间:%f" % self.refresh_rate)
                except ValueError as e:
                    print(e)
            last_vsync_time = 0
            begin_flag = True
            while True:
                if self._stop:
                    q.put("over")
                    break
                before = time.time()
                ignore_line = 0
                timestamps = []
                new_timestamps = []
                r = os.popen("adb -s %s shell dumpsys gfxinfo  %s framestats" % (self.device, self.pkg))
                for line in r.readlines():
                    gfxinfo.write(line)
                    if "---PROFILEDATA---" in line:
                        ignore_line += 1
                    if 1 <= ignore_line < 2:
                        if "---PROFILEDATA---" in line or "GpuCompleted" in line:
                            pass
                        else:
                            # ['IntendedVsync', 'Vsync', 'FrameCompleted']
                            info_data = [line.strip().split(",")[1], line.strip().split(",")[2],
                                         line.strip().split(",")[13]]
                            timestamp = [int(item) / self.nanoseconds_per_second for item in info_data]
                            timestamps.append(timestamp)
                print(last_vsync_time)
                for item in timestamps:
                    if item[1] > last_vsync_time:
                        new_timestamps.append(item)
                if len(timestamps) > 0:
                    if not begin_flag:
                        new_timestamps = [[0, last_vsync_time, 0]] + new_timestamps
                    begin_flag = False
                    last_vsync_time = timestamps[-1][1]  # 更新最后Vsync时间
                cost_time = time.time() - before
                if cost_time < self.freq:
                    time.sleep(self.freq - cost_time)
                print(len(new_timestamps), "-->", new_timestamps)
                print(len(timestamps), "==>", timestamps)
                cur = timestamp_ymd_hms()
                q.put([cur, self.refresh_rate, new_timestamps])

    def terminate(self):
        self._stop = True
