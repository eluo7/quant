import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict

def plot_portfolio_metrics(symbol: str, daily_stats: pd.DataFrame) -> None:
    """绘制投资组合指标"""
    fig = make_subplots(
        rows=4, cols=1,
        subplot_titles=('投资组合价值', '持仓数量', '收益率', '回撤'),
        vertical_spacing=0.05
    )
    
    # 总资产曲线
    fig.add_trace(
        go.Scatter(x=daily_stats.index, y=daily_stats['Total_Value'],
                  name='总资产'),
        row=1, col=1
    )
    
    # 持仓数量
    fig.add_trace(
        go.Scatter(x=daily_stats.index, y=daily_stats['Position'],
                  name='持仓数量'),
        row=2, col=1
    )
    
    # 收益率
    fig.add_trace(
        go.Scatter(x=daily_stats.index, y=daily_stats['Returns'].cumsum(),
                  name='累计收益率'),
        row=3, col=1
    )
    
    # 回撤
    fig.add_trace(
        go.Scatter(x=daily_stats.index, y=daily_stats['Drawdown'],
                  name='回撤', fill='tozeroy'),
        row=4, col=1
    )
    
    fig.update_layout(height=1000, title_text=f"{symbol} 投资组合分析")
    fig.show()

def print_backtest_results(symbol: str, results: Dict) -> None:
    """打印回测结果"""
    print(f"\n{symbol} 回测结果:")
    
    # 打印风险指标
    print("\n风险指标:")
    print(f"总收益率: {results['total_return']:.2%}")
    print(f"最大回撤: {results['max_drawdown']:.2%}")
    print(f"最终收益率: {results['final_capital']:.2%}")