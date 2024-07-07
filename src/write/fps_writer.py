#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @file name: fps_writer.py
 @desc:
 @author: xu wang
 @mail: jason_wangxu@163.com
 @date: 2024/6/23 8:59
"""

import csv
import xlsxwriter
from numpy import mean
from src.common import *
from src.write.writer import Writer


class FpsWriter(Writer):
    def __init__(self, pkg, save, data):
        super().__init__(self, pkg, save, data)
        self.head = ['时间', 'FPS', 'jank']
        self.csv_name = "fps.csv"
        self.xlsx_name = "FPS-" + str(self.pkg).replace(":", "_") + "-" + self.save.split("-")[-1] + ".xlsx"
        self.jank_threshold = 0

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
        生成cpu数据xlsx
        :return:
        """
        rows = self._read_csv(self.csv_name)
        new_save = os.path.join(self.save, name)
        fps = []
        jank = []
        workbook = xlsxwriter.Workbook(new_save)
        try:
            worksheet = workbook.add_worksheet("data")
            worksheet.set_column('A:A', 20)  # 设置列宽
            # 自定义样式，加粗
            style = workbook.add_format()
            style.set_font("等线")
            style.set_num_format('0.0')  # 格式化数据格式为小数点后两位
            style.set_align('center')  # 设置对齐方式
            for i, row in enumerate(rows):
                for j, item in enumerate(row):
                    try:
                        worksheet.write(i, j, float(item), style)
                    except ValueError:
                        worksheet.write(i, j, item, style)
                    if j == 2 and i != 0:
                        fps.append(float(item))
                    if j == 3 and i != 0:
                        jank.append(float(item))
            # 写入最大值和平均值
            fps_max = max(fps)
            fps_avg = mean(fps)
            jank_max = max(jank)
            jank_avg = mean(jank)
            size = len(rows[0])
            worksheet.write(0, size + 1, "fps最大值：%.1f" % fps_max, style)
            worksheet.write(1, size + 1, "fps平均值：%.1f" % fps_avg, style)
            worksheet.write(20, size + 1, "jank最大值：%.1f" % jank_max, style)
            worksheet.write(21, size + 1, "jank平均值：%.1f" % jank_avg, style)
            # 生成整机fps折线图
            chart = workbook.add_chart({'type': 'line'})
            chart.set_title({'name': "%s fps" % self.pkg})
            chart.set_x_axis({'name': "时间(s)"})
            chart.set_y_axis({'name': "数值"})
            chart.add_series({
                'name': '=data!$C$1',
                'categories': f'=data!$A$2:$A${len(fps)}',
                'values': f'=data!$C$2:$C${len(fps)}',
            })
            worksheet.insert_chart(0, size + 4, chart)
            # 生成应用jank折线图
            chart = workbook.add_chart({'type': 'line'})
            chart.set_title({'name': "%s jank" % self.pkg})
            chart.set_x_axis({'name': "时间(s)"})
            chart.set_y_axis({'name': "数值"})
            chart.add_series({
                'name': '=data!$D$1',
                'categories': f'=data!$A$2:$A${len(jank)}',
                'values': f'=data!$D$2:$D${len(jank)}',
            })
            worksheet.insert_chart(20, size + 4, chart)

        finally:
            workbook.close()

    def _write_csv(self, name):
        _flag = True
        head = ['datetime', "package_name", "fps", "jank"]
        save = os.path.join(self.save, name)
        with open(save, 'a+') as df:
            while True:
                row_data = []
                info_list = self.data.get()
                stamp = info_list[0]
                row_data.append(stamp)
                row_data.append(self.pkg)
                self.jank_threshold = info_list[1]
                info = info_list[2]
                fps_value, jank_value = self.calculate_fps_jank(info)
                row_data.append(fps_value)
                row_data.append(jank_value)
                if _flag:
                    csv.writer(df, lineterminator='\n').writerow(head)
                    _flag = False
                if info_list == "over":
                    break
                csv.writer(df, lineterminator='\n').writerow(row_data)

    def calculate_fps_jank(self, timestamps):
        """Returns a list of SurfaceStatsCollector.Result.
        不少手机第一列  第三列 数字完全相同
        """
        frame_count = len(timestamps)
        if frame_count == 0:
            fps = 0
            jank = 0
        elif frame_count == 1:
            fps = 1
            jank = 0
        elif frame_count == 2 or frame_count == 3 or frame_count == 4:
            seconds = timestamps[-1][1] - timestamps[0][1]
            if seconds > 0:
                fps = int(round((frame_count - 1) / seconds))
                jank = self.calculate_jank(timestamps)
            else:
                fps = 1
                jank = 0
        else:
            seconds = timestamps[-1][1] - timestamps[0][1]
            if seconds > 0:
                fps = int(round((frame_count - 1) / seconds))
                jank = self.calculate_jank_new(timestamps)
            else:
                fps = 1
                jank = 0
        logger.info("fps: %d, jank:%d" % (fps, jank))
        return fps, jank

    def calculate_jank(self, timestamps):
        temp_stamp = 0
        # 统计丢帧卡顿
        jank = 0
        for timestamp in timestamps:
            if temp_stamp == 0:
                temp_stamp = timestamp[1]
                continue
            # 绘制帧耗时
            cost_time = timestamp[1] - temp_stamp
            # 耗时大于阈值10个时钟周期,用户能感受到卡顿感
            if cost_time > self.jank_threshold * 10:
                jank = jank + 1
            temp_stamp = timestamp[1]
        return jank

    def calculate_jank_new(self, timestamps):
        """
        同时满足两个条件计算为一次卡顿：
        ①Display FrameTime>前三帧平均耗时2倍。
        ②Display FrameTime>两帧电影帧耗时 (1000ms/24*2≈83.33ms)。
        :param timestamps:
        :return:
        """
        two_film_stamp = 83.3 / 1000.0
        temp_stamp = 0
        # 统计丢帧卡顿
        jank = 0
        for index, timestamp in enumerate(timestamps):
            # 前面四帧按超过166ms计算为卡顿
            if (index == 0) or (index == 1) or (index == 2) or (index == 3):
                if temp_stamp == 0:
                    temp_stamp = timestamp[1]
                    continue
                # 绘制帧耗时
                cost_time = timestamp[1] - temp_stamp
                # 耗时大于阈值10个时钟周期,用户能感受到卡顿感
                if cost_time > self.jank_threshold * 10:
                    jank = jank + 1
                temp_stamp = timestamp[1]
            elif index > 3:
                current_stamp = timestamps[index][1]
                last_one_stamp = timestamps[index - 1][1]
                last_two_stamp = timestamps[index - 2][1]
                last_three_stamp = timestamps[index - 3][1]
                last_four_stamp = timestamps[index - 4][1]
                double_avg_stamp = ((last_three_stamp - last_four_stamp) + (last_two_stamp - last_three_stamp) + (
                        last_one_stamp - last_two_stamp)) / 3 * 2
                current_frame_time = current_stamp - last_one_stamp
                if (current_frame_time > double_avg_stamp) and (current_frame_time > two_film_stamp):
                    jank = jank + 1
        return jank
