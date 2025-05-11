# 量化交易策略框架

## 项目简介
这是一个基于Python的量化交易策略框架，集成了数据获取、技术指标计算、策略回测和可视化功能。

## 技术栈
- 数据获取：yfinance
- 技术指标：TA-Lib
- 回测引擎：vectorbt
- 数据可视化：Plotly

## 项目结构
```
quant/
├── core/                    # 核心功能模块
│   ├── data_handler.py      # 数据获取与管理
│   └── indicator_calculator.py # 技术指标计算
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
