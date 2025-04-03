from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import time
import numpy as np
from typing import Callable, Dict, Tuple, Union, Optional, List
import copy

@dataclass
class BarData(object):
    """
    Candlestick bar data of a certain trading period.
    """
    ticker: str = ""
    start_time: int = 0
    end_time: int = 0
    interval: int = 0
    open: float = 0
    high: float = 0
    low: float = 0
    close: float = 0
    volume: float = 0


class KLineGenerator:
    def __init__(self, ticker:str, snapshot_interval:int, slice_per_sec:int, intervals: List[int]):
        """
        初始化多周期K线生成器
        :param intervals: K线周期列表（单位：秒），例如[60, 300]表示1分钟和5分钟
        """
        self.ticker = ticker
        self.slice_per_sec = slice_per_sec
        self.snapshot_interval = snapshot_interval
        self.intervals: List[int] = intervals
        self.current_klines: Dict[int, BarData] = {}  # 当前未闭合K线
        self.history: Dict[int, List[BarData]] = {}   # 历史K线存储
        self.on_window_bar:Callable = None
        """初始化数据结构"""
        for interval in self.intervals:
            self.current_klines[interval] = BarData()
            self.history[interval] = []

    def set_call_back(self, on_window_bar: Callable):
        self.on_window_bar = on_window_bar

    def _calculate_window_start(self, timestamp: int, interval: int) -> int:
        """计算时间窗口起始时间"""
        timestamp_sec:int = timestamp // 1000
        original = time.localtime(timestamp_sec)
        if interval >= 86400:
            local_tm = time.struct_time((
                original.tm_year,    # 年
                original.tm_mon,      # 月
                original.tm_mday,      # 修改日为 15
                0,     # 时
                0,      # 分
                0,      # 秒
                original.tm_wday,     # 星期几（会自动根据日期调整）
                original.tm_yday,     # 一年中的第几天（会自动调整）
                original.tm_isdst     # 夏令时标志
            ))
        else:
            total_sec:int = original.tm_hour * 3600 + original.tm_min * 60 + original.tm_sec
            aligned_sec:int = (total_sec // interval) * interval
            local_tm = time.struct_time((
                original.tm_year,    # 年
                original.tm_mon,      # 月
                original.tm_mday,      # 修改日为 15
                aligned_sec // 3600,     # 时
                (aligned_sec % 3600) // 60,      # 分
                aligned_sec % 60,      # 秒
                original.tm_wday,     # 星期几（会自动根据日期调整）
                original.tm_yday,     # 一年中的第几天（会自动调整）
                original.tm_isdst     # 夏令时标志
            ))

        return time.mktime(local_tm) * 1000

    def process_tick(self, section_start:int, section_end:int, timestamp:int, price:float, volume:int):
        """
        处理实时Tick数据
        """
        for interval in self.intervals:
            window_start = self._calculate_window_start(timestamp, interval) 
            if self.slice_per_sec > 0:
                window_end = window_start + (interval - 1) * 1000 + (1000 // self.slice_per_sec) * (self.slice_per_sec - 1)
            else:
                window_end = window_start + (interval - self.snapshot_interval) * 1000
            current_kline = self.current_klines[interval]
            # Tick数据在周期内
            if current_kline.end_time > window_start:
                if current_kline.volume > 0:
                    # 更新当前K线
                    current_kline.high = max(current_kline.high, price)
                    current_kline.low = min(current_kline.low, price)
                    current_kline.close = price
                    current_kline.volume += volume
                else:
                    current_kline.open = price
                    current_kline.high = price
                    current_kline.low = price
                    current_kline.close = price
                    current_kline.volume = volume
                # 周期内最后一个Tick切片数据, 关闭K线
                if timestamp >= current_kline.end_time:
                    if section_start + 59 * 1000 <= timestamp and timestamp < section_end + 59 * 1000:
                        self.history[interval].append(copy.copy(current_kline)) 
                        if self.on_window_bar:
                            self.on_window_bar(current_kline)
                    # 初始化新的K线
                    current_kline.ticker = self.ticker
                    current_kline.start_time = self._calculate_window_start(timestamp + 1000, interval)
                    if self.slice_per_sec > 0:
                        current_kline.end_time = current_kline.start_time + (interval - 1) * 1000 + (1000 // self.slice_per_sec) * (self.slice_per_sec - 1)
                    else:
                        current_kline.end_time = current_kline.start_time + (interval - self.snapshot_interval) * 1000
                    current_kline.interval = interval
                    current_kline.open = 0
                    current_kline.high = 0
                    current_kline.low = 0
                    current_kline.close = 0
                    current_kline.volume = 0
            # 第一次初始化K线
            elif current_kline.end_time == 0:
                # 初始化新K线
                current_kline.ticker = self.ticker
                current_kline.start_time = window_start
                current_kline.end_time = window_end
                current_kline.interval = interval
                current_kline.open = price
                current_kline.high = price
                current_kline.low = price
                current_kline.close = price
                current_kline.volume = volume
            # 超时关闭K线
            elif(current_kline.end_time < window_start):
                if section_start + 59 * 1000 <= timestamp and timestamp < section_end + 59 * 1000:
                    # 关闭当前K线
                    self.history[interval].append(copy.copy(current_kline))
                    if self.on_window_bar:
                        self.on_window_bar(current_kline)
                # 初始化新K线
                current_kline.ticker = self.ticker
                current_kline.start_time = window_start
                current_kline.end_time = window_end
                current_kline.interval = interval
                current_kline.open = price
                current_kline.high = price
                current_kline.low = price
                current_kline.close = price
                current_kline.volume = volume

    def close_kline(self, section_start:int, section_end:int, timestamp: int):
        """检查并闭合超时的K线"""
        for interval in self.intervals:
            current_kline = self.current_klines.get(interval)
            # 超时关闭K线
            if timestamp >= current_kline.end_time:
                self.history[interval].append(copy.copy(current_kline))
                if self.on_window_bar:
                    self.on_window_bar(current_kline)

                timestamp = timestamp + 1000
                window_start:int = self._calculate_window_start(timestamp, interval)
                if self.slice_per_sec > 0:
                    window_end:int = window_start + (interval - 1) * 1000 + (1000 // self.slice_per_sec) * (self.slice_per_sec - 1)
                else:
                    window_end:int = window_start + (interval - self.snapshot_interval) * 1000
                # 初始化新K线
                current_kline.ticker = self.ticker
                current_kline.start_time = window_start
                current_kline.end_time = window_end
                current_kline.interval = interval
                current_kline.open = 0
                current_kline.high = 0
                current_kline.low = 0
                current_kline.close = 0
                current_kline.volume = 0

    def flush(self):
        for interval in self.intervals:
            current_kline = self.current_klines.get(interval)
            self.history[interval].append(copy.copy(current_kline))
            current_kline.open = 0
            current_kline.high = 0
            current_kline.low = 0
            current_kline.close = 0
            current_kline.volume = 0

    def get_current_kline(self, interval: int) -> Union[dict, None]:
        """获取当前未闭合的K线"""
        return self.current_klines.get(interval, None)

    def get_history(self, interval: int, limit: int = None) -> List[dict]:
        """获取历史K线数据"""
        history = self.history.get(interval, [])
        return history[-limit:] if limit else history

    def get_close(self, interval: int):
        history_list = self.get_history(interval)
        closes = np.array([bar.close for bar in history_list], dtype=np.float64)
        return closes



# 使用示例
if __name__ == "__main__":

    # 初始化生成器
    kline_generator = KLineGenerator(ticker="al2505", snapshot_interval=0, slice_per_sec=2, intervals=[60, 300, 600, 900, 1800])

    start_time = int(time.time()) * 1000
    section_start = start_time
    section_end = start_time + 1000 * 1000
    # 处理实时数据
    for i in range(0, 1000):
        timestamp:int = start_time + i * 500
        price:float = 100.0 + (i % 20 - 10) * 0.5
        volume:int = 100
        kline_generator.process_tick(section_start, section_end, timestamp, price, volume)
        
        if (timestamp // 1000) % 60 == 0:
            kline_generator.close_kline(section_start, section_end, timestamp)

    kline_generator.flush()
    # 获取完整历史数据
    history_1min = kline_generator.get_history(60)
    for bar in history_1min:
        print(bar)
    history_5min = kline_generator.get_history(300)
    for bar in history_5min:
        print(bar)
    print(kline_generator.get_close(60))