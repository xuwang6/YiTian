#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @file name: boot_writer.py
 @desc:
 @author: xu wang
 @mail: jason_wangxu@163.com
 @date: 2024/6/23 9:09
"""
"""
    @file name：excel_factory
    @desc ：
    @author：王旭
    @mail：wx370782@alibaba-inc.com
    @date：2022/4/13 22:16
"""

import xlsxwriter
from numpy import mean
from src.write.writer import Writer


class BootWriter(Writer):
    def __init__(self, pkg, save, data):
        Writer.__init__(self, pkg, save, data)
        self.head = ['时间', '耗时']

    def write_excel(self):

        """
        数据写入excel文件
        :return:
        """
        workbook = xlsxwriter.Workbook(self.save)
        try:
            worksheet = workbook.add_worksheet("data")
            worksheet.set_column('A:A', 15)  # 设置列宽
            # 自定义样式，加粗
            style = workbook.add_format()
            style.set_font("等线")
            style.set_num_format('0.00')  # 格式化数据格式为小数点后两位
            style.set_align('center')  # 设置对齐方式
            worksheet.write_row('A1', self.head, style)  # 写入表头
            line = 1
            cost_list = []
            while True:
                info_list = self.data.get()
                if info_list == "over":
                    break
                for index, value in enumerate(info_list):
                    if index == 1:
                        cost_list.append(value)
                    worksheet.write(line, index, value, style)
                line = line + 1
            # 写入最大值和平均值
            cost_max = max(cost_list)
            cost_avg = mean(cost_list)

            worksheet.write(0, 4, "启动耗时最大值：%f" % cost_max, style)
            worksheet.write(1, 4, "启动耗时平均值：%.2f" % cost_avg, style)

            # 生成耗时折线图
            name = self.save.split(".")[0].split("-")[-1]
            chart = workbook.add_chart({'type': 'line'})
            chart.set_title({'name': "%s APP启动耗时" % name})
            chart.set_x_axis({'name': "时间(s)"})
            chart.set_y_axis({'name': "数值"})
            chart.add_series({
                'name': '=data!$B$1',
                'categories': f'=data!$A$2:$A${len(cost_list)}',
                'values': f'=data!$B$2:$B${len(cost_list)}',
            })
            worksheet.insert_chart(0, 7, chart)
        finally:
            workbook.close()

    def write_txt(self):
        """
        数据写入txt文件
        :return:
        """
        pass

    def generate_xlsx(self):
        pass
