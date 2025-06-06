from typing import Dict, Optional
import pandas as pd
from .base_strategy import BaseStrategy

class MACrossStrategy(BaseStrategy):
    """均线交叉策略（单股票版本）"""
    
    def __init__(
        self,
        start_date: str,
        end_date: Optional[str] = None,
        params: Dict = None
    ):
        """
        初始化均线交叉策略
        
        参数:
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
            
        super().__init__(start_date, end_date, default_params)
    
    def generate_signals(self) -> Dict[str, pd.DataFrame]:
        """生成交易信号（单股票）"""
        # 获取股票数据
        df = self.data.copy()
        
        # 计算移动平均线
        df[f'ma{self.params["fast_period"]}'] = df['Close'].rolling(
            window=self.params['fast_period']
        ).mean()
        df[f'ma{self.params["slow_period"]}'] = df['Close'].rolling(
            window=self.params['slow_period']
        ).mean()
        
        # 生成信号
        fast_ma = f'ma{self.params["fast_period"]}'
        slow_ma = f'ma{self.params["slow_period"]}'
        
        # 计算金叉和死叉
        df['signal'] = 0
        df.loc[df[fast_ma] > df[slow_ma], 'signal'] = 1  # 金叉
        df.loc[df[fast_ma] < df[slow_ma], 'signal'] = -1  # 死叉
        
        return df


if __name__ == "__main__":
    # 获取测试数据
    test_data = pd.read_csv("../data/cache/AAPL_2024-05-11_2025-05-11_1d.csv")
    start_date = test_data['Date'].iloc[0]
    end_date = test_data['Date'].iloc[-1]

    # 初始化策略
    strategy = MACrossStrategy(
        start_date=start_date,
        end_date=end_date,
        params={'window': 20}
    )
    strategy.set_data(test_data)
    
    # 生成信号
    signals = strategy.generate_signals()
    
    # 打印结果
    print("生成的信号数据:")
    print(signals.tail(20))
