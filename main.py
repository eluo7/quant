from .core.data_collector import DataCollector
from .strategy.ma_cross_strategy import MACrossStrategy
from .backtesting.backtest_engine import BacktestEngine
from .visualization.plot_utils import plot_portfolio_metrics, print_backtest_results
from datetime import datetime, timedelta

def run_backtest(symbol: str, start_date: str, end_date: str = None, strategy_params: dict = None) -> None:
    """运行回测流程"""
    
    # 1. 获取数据
    handler = DataCollector(data_source="polygon")
    print(f"正在获取数据: {symbol}")
    data = handler.fetch_data(symbol, start_date, end_date)

    # 2. 生成交易信号
    print("正在生成交易信号...")
    strategy = MACrossStrategy(
        start_date=start_date,
        end_date=end_date,
        params=strategy_params
    )    
    strategy.set_data(data)
    signals = strategy.generate_signals()

    # 4. 执行回测
    backtest_engine = BacktestEngine()
    print("正在执行回测...")
    results = backtest_engine.run(symbol, signals)
    print(results)

    # 5. 展示回测结果
    # 打印回测结果
    print_backtest_results(symbol, results[symbol])

if __name__ == "__main__":
    # 运行示例
    symbol = 'HOOD'
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    strategy_params = {
        'fast_period': 5,
        'slow_period': 20
    }
    
    run_backtest(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        strategy_params=strategy_params
    )