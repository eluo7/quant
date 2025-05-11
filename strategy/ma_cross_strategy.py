from typing import Dict, List, Optional
import pandas as pd
from .base_strategy import BaseStrategy

class MACrossStrategy(BaseStrategy):
    """均线交叉策略"""
    
    def __init__(
        self,
        symbols: List[str],
        start_date: str,
        end_date: Optional[str] = None,
        params: Dict = None
    ):
        """
        初始化均线交叉策略
        
        参数:
            symbols: 交易品种列表
            start_date: 起始日期
            end_date: 结束日期
            params: 策略参数，包括：
                - fast_period: 快线周期
                - slow_period: 慢线周期
        """
        default_params = {
            'fast_period': 5,
            'slow_period': 20
        }
        if params:
            default_params.update(params)
            
        super().__init__(symbols, start_date, end_date, default_params)
    
    def generate_signals(self) -> Dict[str, pd.DataFrame]:
        """生成交易信号"""
        signals = {}
        for symbol, df in self.data.items():
            # 计算移动平均线
            df = df.copy()
            df[f'MA{self.params["fast_period"]}'] = df['Close'].rolling(
                window=self.params['fast_period']
            ).mean()
            df[f'MA{self.params["slow_period"]}'] = df['Close'].rolling(
                window=self.params['slow_period']
            ).mean()
            
            # 生成信号
            fast_ma = f'MA{self.params["fast_period"]}'
            slow_ma = f'MA{self.params["slow_period"]}'
            
            # 计算金叉和死叉
            df['signal'] = 0
            df.loc[df[fast_ma] > df[slow_ma], 'signal'] = 1  # 金叉
            df.loc[df[fast_ma] < df[slow_ma], 'signal'] = -1  # 死叉
            
            # 只在交叉点产生信号
            df['position_changed'] = df['signal'].diff() != 0
            df.loc[~df['position_changed'], 'signal'] = 0
            
            # 保留必要的列
            signals[symbol] = df[['Close', fast_ma, slow_ma, 'signal']]
            
        return signals