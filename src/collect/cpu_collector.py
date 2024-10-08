#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : cpu_collector.py
# Author            : jason_wangxu@163.com
# Date              : 2024/6/8 14:43
# Last Modified     : 2024/6/8 14:43
# Description       :
#
# Copyright (c) 2024, All rights reserved.


import queue
import subprocess
import threading
from re import split, compile
from src.collect.collector import Collector
from src.write.writer_factory import WriterFactory
from src.common import *


class CpuCollector(Collector):
    """
    CPU数据收集
    """

    def __init__(self, device, pkg, save, event):
        super().__init__()
        self.device = device
        self.pkg = pkg
        self.save = save
        self.event = event
        self._stop = False
        self.dur = 1.0
        self.RE_CPU = compile(
            r'(\d+)\%cpu\s+(\d+)\%user\s+(\d+)\%nice\s+(\d+)\%sys\s+(\d+)\%idle\s+(\d+)\%iow\s+(\d+)\%irq\s+('
            r'\d+)\%sirq\s+(\d+)\%host')

    def executor(self) -> None:
        """
        监控CPU
        :return:
        """
        self.event.wait()
        _flag = True
        pid_list = []
        q = queue.Queue()
        #   写入excel
        factory = WriterFactory(self.pkg, self.save, q)
        t = threading.Thread(target=factory.write_data, args=["CPU"])
        t.start()
        cmd = f"adb -s {self.device} shell top -b -d {self.dur}"
        for index, item in enumerate(self.pkg):
            pid = self._get_pid(item)
            if pid == 0:
                logger.debug(f"未发现应用{item}，请确认是否正常运行！！")
                return
            pid_list.append(pid)
            # cmd = cmd + f" -p {pid}"
        logger.debug("PID列表：%s" % str(pid_list))
        logger.debug("执行的命令：%s" % cmd)
        data_list = list(zip(pid_list, self.pkg))
        cpu_data = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        info = None
        tmp_list = None
        total_cpu_rate = 0

        with open(os.path.join(self.save, "top.log"), mode="w", encoding="utf-8") as f:
            while True:
                if self._stop:
                    q.put("over")
                    cpu_data.terminate()
                    break
                cpu_line = cpu_data.stdout.readline().strip()
                f.write(cpu_line + "\n")
                if _flag:
                    info = []
                    tmp_list = []
                    cur = timestamp_hms()
                    info.append(cur)
                    if "Tasks:" in cpu_line or "Mem:" in cpu_line or "Swap:" in cpu_line or "TIME+" in cpu_line:
                        logger.debug("跳过头************ %s" % cpu_line)
                        continue
                    if cpu_line == "":
                        logger.debug("跳过空行************")
                        continue
                    if "%user" in cpu_line:
                        match = self.RE_CPU.search(cpu_line)
                        if match:
                            logger.debug(f"整机CPU------> {cpu_line}")
                            cpu_rate = match.group(1)
                            user_rate = match.group(2)
                            nice_rate = match.group(3)
                            system_rate = match.group(4)
                            idle_rate = match.group(5)
                            iow_rate = match.group(6)
                            irq_rate = match.group(7)
                            sirq_rate = match.group(8)
                            host_rate = match.group(9)
                            continue
                    info.append(cpu_rate)
                    info.append(user_rate)
                    info.append(nice_rate)
                    info.append(system_rate)
                    info.append(idle_rate)
                    info.append(iow_rate)
                    info.append(irq_rate)
                    info.append(sirq_rate)
                    info.append(host_rate)
                    logger.debug("整机********* %s", str(info))
                for item in data_list:
                    if item[0] in cpu_line and cpu_line.endswith(item[1]):
                        pid_data_list = []
                        logger.debug(f"进程CPU------> {cpu_line}")
                        items = split(r"\s+", cpu_line.strip())
                        cpu_app_rate = float(items[-4])
                        pid_data_list.append(item[0])
                        pid_data_list.append(item[1])
                        pid_data_list.append(cpu_app_rate)
                        data_list.remove(item)
                        logger.debug("pid_data_list ---> %s, data_list ---> %s" % (str(pid_data_list), str(data_list)))
                        total_cpu_rate += cpu_app_rate
                        break
                else:
                    logger.debug("跳过无用进程******** %s" % cpu_line)
                    continue
                if len(pid_data_list) != 0:
                    tmp_list.append(pid_data_list)
                else:
                    logger.debug(f"有进程找不到了，请检测各PID是否发生了变化 -_-！！")
                    return
                if len(data_list) != 0:
                    _flag = False
                    logger.debug("PID中间状态------>%s" % str(tmp_list))
                    continue
                else:
                    _flag = True
                    data_list = list(zip(pid_list, self.pkg))
                    tmp_list = sorted(tmp_list, key=lambda x: int(x[0]))
                    logger.debug("PID最后状态------>%s" % str(tmp_list))
                for item in tmp_list:
                    info = info + item
                info.append(total_cpu_rate)
                logger.info(f"CPU信息 ---> {info}")
                logger.debug("queue==> %s" % info)
                q.put(info)
                total_cpu_rate = 0

    def terminate(self):
        self._stop = True
