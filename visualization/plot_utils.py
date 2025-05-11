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
    metrics = results['risk_metrics']
    print(f"总收益率: {metrics['total_return']:.2%}")
    print(f"年化收益率: {metrics['annual_return']:.2%}")
    print(f"夏普比率: {metrics['sharpe_ratio']:.2f}")
    print(f"最大回撤: {metrics['max_drawdown']:.2%}")
    
    # 打印交易统计
    print("\n交易统计:")
    stats = results['trade_stats']
    print(f"总交易次数: {stats['total_trades']}")
    print(f"胜率: {stats['win_rate']:.2%}")
    print(f"平均盈利: ${stats['avg_win']:.2f}")
    print(f"平均亏损: ${stats['avg_loss']:.2f}")
    print(f"平均持仓时间: {stats['avg_hold_time']:.1f} 天")