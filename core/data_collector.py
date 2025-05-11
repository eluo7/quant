import yfinance as yf
import pandas as pd
from typing import List, Dict, Optional, Protocol
import os
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from polygon import RESTClient

# 加载环境变量，强制覆盖已存在的环境变量
load_dotenv(override=True)

class DataSource(ABC):
    """数据源抽象基类"""

    @abstractmethod
    def fetch_history(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        """获取历史数据"""
        pass

class YFinanceSource(DataSource):
    """YFinance数据源实现"""
    
    def fetch_history(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(
                start=start_date,
                end=end_date,
                interval=interval
            )
            return df if not df.empty else None
        except Exception as e:
            print(f"YFinance获取{symbol}数据失败: {e}")
            return None

class PolygonSource(DataSource):
    """Polygon.io数据源实现"""
    
    def __init__(self, api_key: str):
        self.client = RESTClient(api_key)
        
    def fetch_history(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        try:
            # 转换日期格式
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            
            # 获取股票数据
            aggs = self.client.get_aggs(
                symbol,
                1,  # 复权因子
                'day' if interval == '1d' else interval,
                start.strftime('%Y-%m-%d'),
                end.strftime('%Y-%m-%d')
            )
            
            if not aggs:
                print(f"Polygon.io未能获取到 {symbol} 的数据")
                return None
            
            # 转换为DataFrame
            df = pd.DataFrame([{
                'Open': agg.open,
                'High': agg.high,
                'Low': agg.low,
                'Close': agg.close,
                'Volume': agg.volume,
                'Date': datetime.fromtimestamp(agg.timestamp/1000)
            } for agg in aggs])
            
            # 设置索引
            df.set_index('Date', inplace=True)
            return df
            
        except Exception as e:
            print(f"Polygon.io获取{symbol}数据失败: {e}")
            return None

class DataCollector:
    """数据获取和管理类（单股票版本）"""
    
    def __init__(self, data_source: str = "polygon", cache_dir: str = "./data/cache", api_keys: Dict[str, str] = None):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
        # 优先从环境变量获取API密钥
        self.api_keys = {}
        if "POLYGON_API_KEY" in os.environ:
            self.api_keys["polygon"] = os.environ["POLYGON_API_KEY"]
        # 如果提供了api_keys参数，则更新或添加新的密钥
        if api_keys:
            self.api_keys.update(api_keys)
            
        # 初始化指定的数据源
        if data_source == "yfinance":
            self.source = YFinanceSource()
        elif data_source == "polygon":
            if "polygon" not in self.api_keys:
                raise ValueError("使用Polygon数据源需要提供API KEY")
            self.source = PolygonSource(self.api_keys["polygon"])
        else:
            raise ValueError(f"不支持的数据源: {data_source}")
    
    def _get_cache_path(self, symbol: str, start: str, end: str, interval: str) -> str:
        """生成缓存文件路径"""
        filename = f"{symbol}_{start}_{end}_{interval}.csv"
        return os.path.join(self.cache_dir, filename)
    
    def fetch_data(self, symbol: str, start_date: str, end_date: Optional[str] = None, interval: str = "1d", use_cache: bool = True) -> Optional[pd.DataFrame]:
        """
        获取股票历史数据（单股票版本）
        
        参数:
            symbol (str): 股票代码，如 'AAPL'
            start_date (str): 开始日期，格式 'YYYY-MM-DD'
            end_date (str, optional): 结束日期，格式 'YYYY-MM-DD'
            interval (str): 数据间隔，默认为日线 '1d'
            use_cache (bool): 是否使用缓存，默认为True
            
        返回:
            Optional[pd.DataFrame]: 股票数据DataFrame，如果获取失败则返回None
        """
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
            
        cache_path = self._get_cache_path(symbol, start_date, end_date, interval)
        
        # 尝试从缓存加载数据
        if use_cache and os.path.exists(cache_path):
            try:
                df = pd.read_csv(cache_path, index_col=0, parse_dates=True)
                print(f"从缓存加载 {symbol} 的数据")
                return df
            except Exception as e:
                print(f"读取缓存文件失败: {e}")
        
        # 从指定数据源获取数据
        df = self.source.fetch_history(
            symbol, start_date, end_date, interval
        )
        
        if df is None:
            print(f"警告: 未能获取到 {symbol} 的数据")
            return None
        else:
            # 保存到缓存
            if use_cache:
                df.to_csv(cache_path)
                print(f"数据已缓存到: {cache_path}")
            return df

# 使用示例
if __name__ == "__main__":
    # 使用 polygon 数据源
    handler = DataCollector(data_source="polygon")
    
    # 获取最近30天的数据
    start = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    end = datetime.now().strftime('%Y-%m-%d')
    
    # 获取单只股票数据
    result = handler.fetch_data('HOOD', start, end)
    print("\n股票数据示例:")
    print(result.head())
        