#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @file name: cpu_writer.py
 @desc:
 @author: xu wang
 @mail: jason_wangxu@163.com
 @date: 2024/6/23 9:07
"""

import csv
import os.path
import numpy
from src.common import *
import xlsxwriter
from numpy import mean
from src.write.writer import Writer


class CpuWriter(Writer):
    def __init__(self, pkg, save, data):
        super().__init__(pkg, save, data)
        self.csv_name = "cpu_top.csv"
        self.xlsx_name = "CPU-" + str(self.pkg).replace(":", "_") + "-" + self.save.split("-")[-1] + ".xlsx"
        # 报告目录路径
        yaml_model = read_yaml(os.path.join(CONFIG_PATH, "run.yaml"))["model"]
        if yaml_model == "V2148A":
            TOTAL_DMIPS = 100000
        else:
            TOTAL_DMIPS = -1
        self.dmips = TOTAL_DMIPS / (adb.cpu_core_num * 100)
        logger.info("设备型号：%s，总算力：%d，百分比转化DMIPS:----->%f" % (yaml_model, TOTAL_DMIPS, self.dmips))
        self.column_dic = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I", 9: "J", 10: "K",
                           11: "L", 12: "M", 13: "N", 14: "O", 15: "P", 16: "Q", 17: "R", 18: "S", 19: "T", 20: "U",
                           21: "V", 22: "W", 23: "X", 24: "Y", 25: "Z", 26: "AA", 27: "AB", 28: "AC", 29: "AD"}

    def generate(self):
        try:
            self._write_csv(self.csv_name)
        finally:
            self._write_excel(self.xlsx_name)

    def _write_excel(self, name):
        """
        生成cpu数据xlsx
        :return:
        """
        rows = self._read_csv(self.csv_name)
        new_save = os.path.join(self.xlsx_name)
        logger.info("文件地址：%s " % new_save)
        workbook = xlsxwriter.Workbook(new_save)
        try:
            worksheet = workbook.add_worksheet("data")
            worksheet.set_column('A:P', 15)  # 设置列宽
            # 自定义样式，加粗
            style = workbook.add_format()
            style.set_font("等线")
            style.set_num_format('0.0')  # 格式化数据格式为小数点后两位
            style.set_align('left')  # 设置对齐方式
            modify_list = []
            graph_list = []
            i, j = 0, 0
            for i, row in enumerate(rows):
                for j, item in enumerate(row):
                    try:
                        if i == 0 and "_cpu" in item:
                            graph_list.append(j)
                        if i == 0 and "%" in item:
                            modify_list.append(j)
                            worksheet.write(i, j, item.replace("%", "[DMIPS]"), style)
                        elif i != 0 and j in modify_list:
                            item = float(item) * self.dmips
                            worksheet.write(i, j, item, style)
                        else:
                            worksheet.write(i, j, item, style)
                    except Exception as e:
                        raise e
            text_addr = 0  # 最大值、平均值位置
            graph_addr = 0  # 折线图位置
            title = ""
            cpu_avg = 0
            for index in graph_list:
                cpu_list = []
                for i, row in enumerate(rows):
                    for j, item in enumerate(row):
                        if i == 1 and j == index - 1 and index != 1 and index != graph_list[-1]:
                            title = item
                        if i == 1 and j == index - 1 and index != 1 and index == graph_list[-1]:
                            title = "Total_PIDs"
                        if i != 0 and j == index:
                            item = float(item) * self.dmips
                            cpu_list.append(item)
                # 写入最大值和平均值
                cpu_max = max(cpu_list)
                cpu_avg = mean(cpu_list)
                cpu_pct90 = numpy.percentile(cpu_list, 90)
                cpu_pct95 = numpy.percentile(cpu_list, 95)
                size = len(rows[0])
                worksheet.write(text_addr, size + 2, "%s\nCPU_最大值：%.2f" % (title, cpu_max), style)
                worksheet.write(text_addr + 1, size + 2, "%s\nCPU_平均值：%.2f" % (title, cpu_avg), style)
                worksheet.write(text_addr + 2, size + 2, "%s\nCPU_90分位值：%.2f" % (title, cpu_pct90), style)
                worksheet.write(text_addr + 3, size + 2, "%s\nCPU_95分位值：%.2f" % (title, cpu_pct95), style)
                # 生成整机CPU折线图
                chart = workbook.add_chart({'type': 'line'})
                chart.set_title({'name': "%s\nCPU占用" % title})
                chart.set_x_axis({'name': "时间(s)"})
                chart.set_y_axis({'name': "数值"})
                chart.add_series({
                    'name': '数值',
                    'categories': f'=data!$A$2:$A${len(cpu_list)}',
                    'values': f'=data!${self.column_dic[index]}$2:${self.column_dic[index]}${len(cpu_list)}',
                })
                worksheet.insert_chart(graph_addr, size + 5, chart)
                text_addr += 20
                graph_addr += 20
            t_column = self.column_dic[j]
            ch_column = self.column_dic[j + 1]
            worksheet.write(f"{ch_column}1", "连续高值")
            print(f"====> 行数：{i},列：{ch_column},平均值：{cpu_avg}")
            for index in range(i):
                worksheet.write_formula(f"{ch_column}{index + 2}",
                                        f'=IF(AND({t_column}{index + 2}>{cpu_avg},{t_column}{index + 3}>{cpu_avg},{t_column}{index + 4}>{cpu_avg}),'
                                        f'AVERAGE({t_column}{index + 2}:{t_column}{index + 4}),0)')
            worksheet.write(f"{self.column_dic[j + 3]}{text_addr + 5 - 20}", "Total_PIDs均峰值：")
            worksheet.write_formula(f"{self.column_dic[j + 4]}{text_addr + 5 - 20}",
                                    f"=AVERAGEIF({ch_column}2:{ch_column}{i + 1},\"<>0\")")
        finally:
            workbook.close()

    def _write_csv(self, name):
        _flag = True
        head = ['datetime', "cpu%", "user%", "nice%", "sys%", "idle%", "iow%", "irq%", "sirq%", "host%", "pid",
                "package", "pid_cpu%"]
        save = os.path.join(self.save, name)
        with open(save, 'a+') as df:
            while True:
                info_list = self.data.get()
                if _flag:
                    size = len(info_list) - 1
                    if size > 8:
                        for index in range(int((size - 13) / 3)):
                            head = head + ["pid%d" % (index + 1), "package%d" % (index + 1),
                                           "pid_cpu%d%%" % (index + 1)]
                    head = head + ['total_pid_cpu%']
                    csv.writer(df, lineterminator='\n').writerow(head)
                    _flag = False
                if info_list == "over":
                    break
                csv.writer(df, lineterminator='\n').writerow(info_list)
