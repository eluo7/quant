# Core 核心功能模块

本目录包含量化交易框架的核心功能实现。

## 模块说明

### data_handler.py
- 实现多数据源支持（YFinance、Polygon.io）
- 数据缓存管理
- 统一的数据获取接口
- 支持主备数据源切换
- 环境变量配置支持

### indicator_calculator.py
- 技术指标计算模块
- 基于 TA-Lib 实现
- 支持 150+ 种技术指标
- 提供指标参数优化功能