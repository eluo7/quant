from abc import ABC, abstractmethod
from typing import Dict, Optional
import pandas as pd
from datetime import datetime

class BaseStrategy(ABC):
    """策略基类，专注于生成交易信号（单股票版本）"""
    
    def __init__(
        self,
        start_date: str,
        end_date: Optional[str] = None,
        params: Dict = None
    ):
        """
        初始化策略
        
        参数:
            start_date: 起始日期
            end_date: 结束日期
            params: 策略参数字典
        """
        self.start_date = start_date
        self.end_date = end_date or datetime.now().strftime('%Y-%m-%d')
        self.params = params or {}
        self.data: Dict[str, pd.DataFrame] = {}  # 保持字典格式以兼容接口
        
    @abstractmethod
    def generate_signals(self) -> Dict[str, pd.DataFrame]:
        """
        生成交易信号
        
        返回:
            Dict[str, pd.DataFrame]: 单个品种的信号DataFrame，
            信号值：1(买入)、0(持仓不变)、-1(卖出)
        """
        pass
    
    def set_data(self, data: Dict[str, pd.DataFrame]) -> None:
        """设置策略数据"""
        self.data = data