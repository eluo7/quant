from core.data_collector import DataCollector
from strategy.ma_cross_strategy import MACrossStrategy
from backtesting.backtest_engine import BacktestEngine
from visualization.plot_utils import plot_portfolio_metrics, print_backtest_results
from datetime import datetime, timedelta

def run_backtest(
    symbols: list,
    start_date: str,
    end_date: str = None,
    strategy_params: dict = None
) -> None:
    """运行回测流程"""
    
    # 1. 初始化组件
    data_handler = DataCollector(data_source="polygon")
    strategy = MACrossStrategy(
        symbols=symbols,
        start_date=start_date,
        end_date=end_date,
        params=strategy_params
    )
    backtest_engine = BacktestEngine()
    
    # 2. 获取数据
    print(f"正在获取数据: {symbols}")
    data = data_handler.fetch_data(symbols, start_date, end_date)
    
    # 3. 生成交易信号
    print("正在生成交易信号...")
    strategy.set_data(data)
    signals = strategy.generate_signals()
    
    # 4. 执行回测
    print("正在执行回测...")
    results = backtest_engine.run(signals, data)
    
    # 5. 展示回测结果
    for symbol in symbols:
        if symbol in results:
            # 打印回测结果
            print_backtest_results(symbol, results[symbol])
            # 绘制图表
            plot_portfolio_metrics(symbol, results[symbol]['daily_stats'])

if __name__ == "__main__":
    # 运行示例
    symbols = ['NVDA']
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    strategy_params = {
        'fast_period': 5,
        'slow_period': 20
    }
    
    run_backtest(
        symbols=symbols,
        start_date=start_date,
        end_date=end_date,
        strategy_params=strategy_params
    )