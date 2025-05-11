from typing import Dict, List, Optional, Union
import pandas as pd
import numpy as np
import vectorbt as vbt
from ..strategy.ma_cross_strategy import MACrossStrategy

class BacktestEngine:
    """回测引擎：专注于执行回测和计算回测指标"""
    
    def __init__(self, initial_capital: float = 100000.0, slippage: float = 0.001):
        """
        初始化回测引擎
        
        参数:
            symbol: 股票代码
            initial_capital: 初始资金
            slippage: 滑点率
        """
        self.initial_capital = initial_capital
        self.slippage = slippage
        
    def run(self, symbol, signals: pd.DataFrame):
        """执行回测并返回结果"""
        portfolio_results = {}
        
        # 复制数据，避免修改原始数据
        df = signals.copy()

        # 确保数据包含必要的列
        if df.empty or 'Open' not in df.columns or 'Close' not in df.columns or 'signal' not in df.columns:
            raise ValueError("Strategy data is invalid or missing required columns")
        
        # 将 signal 转换为 VectorBT 所需的 entry 和 exit 信号
        long_entries = df['signal'] == 1
        long_exits = df['signal'] == -1
        
        # 信号偏移一天（今天信号，明天执行）
        long_entries = long_entries.shift(1, fill_value=False)
        long_exits = long_exits.shift(1, fill_value=False)
        
        # 使用下一交易日的开盘价作为交易执行价格
        next_open_prices = df['Open'].shift(-1)
        
        # 使用 VectorBT 的 Portfolio.from_signals 创建回测组合
        portfolio = vbt.Portfolio.from_signals(
            close=df['Close'],
            open=df['Open'],
            entries=long_entries,
            exits=long_exits,
            short_entries=False,
            short_exits=False,
            price=next_open_prices,
            init_cash=self.initial_capital,
            size=100,  # 固定每次交易100股
            slippage=self.slippage,
            freq='1D',
            size_type='amount'
        )
        
        # 计算交易价格（用于模拟和现实对比）
        df['trade_price'] = np.nan
        df.loc[long_entries, 'trade_price'] = next_open_prices * (1 + self.slippage)
        df.loc[long_exits, 'trade_price'] = next_open_prices * (1 - self.slippage)
        
        # 资金变化
        df['Capital'] = portfolio.value()
        
        # 获取回测结果
        total_return = portfolio.total_profit()
        max_drawdown = portfolio.max_drawdown() * self.initial_capital
        final_capital = portfolio.value().iloc[-1]
        
        # 输出信息
        print(f"Portfolio Stats:\n", portfolio.stats())
        print(f"trade_price Head:\n", df[['Open', 'signal', 'trade_price']].head(10))
        print(f"Trades:\n", portfolio.trades.records_readable)
        
        # 整理结果
        results = {
            'total_return': total_return,
            'max_drawdown': max_drawdown,
            'final_capital': final_capital,
            'backtest_data': df,
            'portfolio': portfolio
        }
        
        portfolio_results[symbol] = results
        
        return portfolio_results

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


    # 初始化回测引擎
    engine = BacktestEngine('AAPL', initial_capital=100000.0, slippage=0.001)
    
    # 执行回测
    results = engine.run(signals)
    
    # 打印结果
    print("回测结果:")
    print(results)