# 大模型量化交易策略框架

## 项目背景
本项目旨在构建一个基于大模型的智能量化交易系统。通过整合多维度的市场数据，包括技术面指标、基本面指标以及舆情信息，结合大语言模型的强大分析能力，为投资决策提供智能化的建议。

系统的核心特点：
1. 多维数据分析：集成技术面（K线、成交量等）、基本面（财务报表、估值指标等）和市场舆情（新闻、社交媒体等）数据
2. 大模型决策：利用大语言模型对多维数据进行综合分析，模拟专业交易员的决策过程
3. 实时适应：根据市场反馈不断优化模型，提高决策准确性

## 项目简介
这是一个基于Python的量化交易策略框架，集成了数据获取、技术指标计算、策略回测和可视化功能。

## 技术栈
- 数据获取：yfinance polygon.io
- 技术指标：TA-Lib
- 回测引擎：vectorbt
- 数据可视化：Plotly

## 项目结构
```
quant/
├── core/                    # 核心功能模块
│   └── data_collector.py    # 数据获取与管理
├── strategies/              # 策略定义
│   ├── base_strategy.py     # 策略基类
│   └── ma_cross_strategy.py # 示例：均线交叉策略
├── backtesting/            # 回测相关
│   └── backtest_engine.py   # 回测引擎
├── visualization/          # 可视化工具
│   └── plot_utils.py       # 绘图工具
├── data/                   # 数据存储
│   └── cache/              # 数据缓存
└── config/                 # 配置文件
└── config.json             # 配置参数
```

## 安装依赖
```bash
pip install yfinance pandas numpy ta-lib vectorbt plotly
```

## 使用说明
1. 数据获取：使用yfinance获取美股数据
2. 技术指标：支持MA、RSI等150+种技术指标
3. 策略回测：使用vectorbt进行高效回测
4. 结果可视化：使用Plotly生成交互式图表

## 配置说明
在使用 Polygon.io 数据源时，需要配置 API 密钥。有两种方式：

1. 环境变量（推荐）：
```bash
export POLYGON_API_KEY="your_api_key"
```
