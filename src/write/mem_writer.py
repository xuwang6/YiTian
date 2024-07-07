#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @file name: mem_writer.py
 @desc:
 @author: xu wang
 @mail: jason_wangxu@163.com
 @date: 2024/6/22 17:39
"""

import csv
import os.path
import numpy
from src.common.log import logger
import xlsxwriter
from numpy import mean
from src.write.writer import Writer


class MemWriter(Writer):
    def __init__(self, pkg, save, data):
        super().__init__(pkg, save, data)
        self.csv_name = "mem_%s.csv" % self.pkg
        self.xlsx_name = "MEM-" + str(self.pkg).replace(":", "_") + "-" + self.save.split("-")[-1] + ".xlsx"

    def generate(self):
        """
        csv转xlsx
        :return:
        """
        try:
            self._write_csv(self.csv_name)
        finally:
            self._write_excel(self.xlsx_name)

    def _write_excel(self, name):
        """
        数据写入excel文件
        :return:
        """
        rows = self._read_csv(self.csv_name)
        new_save = os.path.join(self.save, name)
        logger.info("文件地址：%s " % new_save)
        head = ['时间', '系统Total', '系统Used', '系统Free', 'PID', 'PID_JavaHeap(MB)', 'PID_NativeHeap(MB)',
                'PID_PSS(MB)']
        workbook = xlsxwriter.Workbook(new_save)
        try:
            worksheet = workbook.add_worksheet("data")
            worksheet.set_column('A:H', 12)  # 设置列宽
            # 自定义样式，加粗
            style = workbook.add_format()
            style.set_font("等线")
            style.set_num_format('0.000')  # 格式化数据格式为小数点后两位
            style.set_align('left')  # 设置对齐方式
            worksheet.write_row('A1', head, style)  # 写入表头
            line, size = 1, 7
            total_list, used_list, free_list = [], [], []
            java_heap_list, native_heap_list, pss_list = [], [], []
            for i, row in enumerate(rows):
                if i == 0:  # 跳过第一行
                    continue
                for index, value in enumerate(row):
                    if index == 0 or index == 1:
                        worksheet.write(line, index, value, style)
                        continue
                    if index == 2:
                        total_list.append(value)
                        worksheet.write(line, index, value, style)
                    if index == 3:
                        used_list.append(value)
                        worksheet.write(line, index, value, style)
                    if index == 4:
                        free_list.append(value)
                        worksheet.write(line, index, value, style)
                    if index == 5:
                        java_heap_list.append(float(value))
                        worksheet.write(line, index, float(value), style)
                    if index == 6:
                        native_heap_list.append(float(value))
                        worksheet.write(line, index, float(value), style)
                    if index == 7:
                        pss_list.append(float(value))
                        worksheet.write(line, index, float(value), style)
                line = line + 1
            # 写入最大值和平均值
            java_heap_max = max(java_heap_list)
            java_heap_avg = mean(java_heap_list)
            native_heap_max = max(native_heap_list)
            native_heap_avg = mean(native_heap_list)
            pss_max = max(pss_list)
            pss_avg = mean(pss_list)
            pss_pct90 = numpy.percentile(pss_list, 90)
            pss_pct95 = numpy.percentile(pss_list, 95)
            worksheet.write(0, size + 1, "PSS最大值：%.2f" % pss_max, style)
            worksheet.write(1, size + 1, "PSS平均值：%.2f" % pss_avg, style)
            worksheet.write(2, size + 1, "PSS 90分位值：%.2f" % pss_pct90, style)
            worksheet.write(3, size + 1, "PSS 95分位值：%.2f" % pss_pct95, style)
            worksheet.write(17, size + 1, "JavaHeap最大值：%.2f" % java_heap_max, style)
            worksheet.write(18, size + 1, "JavaHeap平均值：%.2f" % java_heap_avg, style)
            worksheet.write(34, size + 1, "NativeHeap最大值：%.2f" % native_heap_max, style)
            worksheet.write(35, size + 1, "NativeHeap平均值：%.2f" % native_heap_avg, style)
            # 生成PSS折线图
            chart = workbook.add_chart({'type': 'line'})
            chart.set_title({'name': f"{self.pkg}  PSS"})
            chart.set_x_axis({'name': "时间(s)"})
            chart.set_y_axis({'name': "数值"})
            chart.add_series({
                'name': '=data!$H$1',
                'categories': f'=data!$A$2:$A${len(pss_list)}',
                'values': f'=data!$H$2:$H${len(pss_list)}',
            })
            worksheet.insert_chart(0, size + 4, chart)
            # 生成Java Heap折线图
            chart = workbook.add_chart({'type': 'line'})
            chart.set_title({'name': f"{self.pkg}  JavaHeap"})
            chart.set_x_axis({'name': "时间(s)"})
            chart.set_y_axis({'name': "数值"})
            chart.add_series({
                'name': '=data!$F$1',
                'categories': f'=data!$A$2:$A${len(java_heap_list)}',
                'values': f'=data!$F$2:$F${len(java_heap_list)}',
            })
            worksheet.insert_chart(17, size + 4, chart)
            # 生成Native Heap折线图
            chart = workbook.add_chart({'type': 'line'})
            chart.set_title({'name': f"{self.pkg}  NativeHeap"})
            chart.set_x_axis({'name': "时间(s)"})
            chart.set_y_axis({'name': "数值"})
            chart.add_series({
                'name': '=data!$G$1',
                'categories': f'=data!$A$2:$A${len(native_heap_list)}',
                'values': f'=data!$G$2:$G${len(native_heap_list)}',
            })
            worksheet.insert_chart(34, size + 4, chart)
        finally:
            workbook.close()

    def _write_csv(self, name):
        head = ['datetime', "total", "used", "free", "pid", "java heap(MB)", "native heap(MB)", "pss(MB)"]
        save = os.path.join(self.save, name)
        with open(save, 'a+') as df:
            csv.writer(df, lineterminator='\n').writerow(head)
            while True:
                info_list = self.data.get()
                if info_list == "over":
                    break
                csv.writer(df, lineterminator='\n').writerow(info_list)
