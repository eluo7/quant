from typing import Dict, Optional
import pandas as pd
from .base_strategy import BaseStrategy
import os

class SimpleMeanReversionStrategy(BaseStrategy):
    """
    简单均值回归策略（单股票版本）
    
    策略逻辑：
    1. 当价格低于移动平均线时买入（认为价格会回归均值）
    2. 当价格高于移动平均线时卖出（认为价格会回归均值）
    """
    
    def __init__(
        self,
        start_date: str,
        end_date: Optional[str] = None,
        params: Dict = None
    ):
        """
        初始化均值回归策略
        
        参数:
            start_date: 起始日期
            end_date: 结束日期
            params: 策略参数，包括：
                - window: 移动平均窗口期
        """
        default_params = {
            'window': 20
        }
        if params:
            default_params.update(params)
            
        super().__init__(start_date, end_date, default_params)
        self.window = default_params['window']
        
    def generate_signals(self) -> Dict[str, pd.DataFrame]:
        """生成交易信号（单股票）"""
        # 获取股票数据
        df = self.data.copy()
        
        # 计算移动平均线
        df['ma'] = df['Close'].rolling(window=self.window).mean()
        
        # 初始化信号列 0:持有, 1:买入, -1:卖出
        df['signal'] = 0
        
        # 当价格低于均线时买入
        df.loc[df['Close'] < df['ma'], 'signal'] = 1
        
        # 当价格高于均线时卖出
        df.loc[df['Close'] > df['ma'], 'signal'] = -1
        
        return df

if __name__ == "__main__":
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(current_dir)

    # 获取测试数据
    test_data = pd.read_csv("../data/cache/AAPL_2024-05-11_2025-05-11_1d.csv")
    start_date = test_data['Date'].iloc[0]
    end_date = test_data['Date'].iloc[-1]

    # 初始化策略
    strategy = SimpleMeanReversionStrategy(
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
