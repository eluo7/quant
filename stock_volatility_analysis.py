import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from core.data_collector import DataCollector
from datetime import datetime, timedelta
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # Mac系统支持的字体
plt.rcParams['axes.unicode_minus'] = False
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def get_stock_data(ticker, n_days):
    # 初始化数据收集器
    collector = DataCollector(data_source="polygon")
    # 设置时间范围
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=n_days)).strftime('%Y-%m-%d')
    # 获取数据
    stock_data = collector.fetch_data(ticker, start_date, end_date)
    return stock_data

# 定义函数计算涨跌分布和分位数
def analyze_volatility(df, input_return, n_days):
    if df is None or 'Close' not in df.columns:
        print('数据获取失败或缺少 Close 列')
        return None, None, None
    historical_returns = df['Close'].pct_change().dropna()[-n_days:]
    percentile = np.percentile(historical_returns, [i for i in range(1, 100)])
    current_percentile = np.sum(historical_returns < input_return) / len(historical_returns)
    return historical_returns, current_percentile, percentile

# 可视化波动率
def visualize_volatility(ticker: str, historical_returns: np.ndarray, input_return: float, n_days: int) -> None:
    """使用Plotly可视化波动率"""
    fig = go.Figure()
    
    # 添加直方图
    fig.add_trace(go.Histogram(
        x=historical_returns,
        name='收益率分布',
        marker=dict(
            color='#1f77b4',
            line=dict(
                width=1,
                color='#0f4870'
            )
        ),
        opacity=0.75,
        histnorm='probability density',
        xbins=dict(size=0.01)
    ))
    
    # 添加收益率线
    fig.add_vline(
        x=input_return,
        line_dash="dash",
        line_color="red",
        annotation_text=f"假设涨幅 {input_return*100:.1f}%"
    )
    
    # 更新布局
    fig.update_layout(
        title=f"{ticker} 近 {n_days} 天波动率分布",
        xaxis_title="股价波动率(%)",
        yaxis_title="频数",
        hovermode="x unified"
    )
    
    # 设置x轴为百分比格式
    fig.update_xaxes(tickformat=".1%")
    
    fig.show()

# 主函数
def main():
    ticker = 'NVDL'
    # 假设涨幅，由用户指定
    input_return = 0.06
    n_days = 365
    # 获取数据
    df = get_stock_data(ticker, n_days)
    if df is not None:
        # 分析波动
        historical_returns, current_percentile, percentile = analyze_volatility(df, input_return, n_days)
        if historical_returns is not None:
            # 输出结果
            print(f'{ticker} 假设涨幅 {input_return * 100}%，则在近 {n_days} 天的走势中，相当于分位数: {current_percentile * 100:.2f}%')
            # 可视化
            visualize_volatility(ticker, historical_returns, input_return, n_days)

if __name__ == '__main__':
    main()