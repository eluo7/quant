import yfinance as yf
import pandas as pd
from typing import List, Dict, Optional, Protocol
import os
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

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
        self.api_key = api_key
        
    def fetch_history(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        # TODO: 实现Polygon.io的数据获取逻辑
        # 需要安装polygon-api-client并使用API KEY
        print("Polygon.io数据源尚未实现")
        return None

class DataHandler:
    """数据获取和管理类"""
    
    def __init__(
        self,
        primary_source: str = "yfinance",
        backup_sources: List[str] = None,
        cache_dir: str = "data/cache",
        api_keys: Dict[str, str] = None
    ):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
        # 优先从环境变量获取API密钥
        self.api_keys = {}
        if "POLYGON_API_KEY" in os.environ:
            self.api_keys["polygon"] = os.environ["POLYGON_API_KEY"]
        # 如果提供了api_keys参数，则更新或添加新的密钥
        if api_keys:
            self.api_keys.update(api_keys)
        self.sources: Dict[str, DataSource] = {}
        
        # 初始化数据源
        if primary_source == "yfinance":
            self.sources["yfinance"] = YFinanceSource()
        elif primary_source == "polygon":
            if "polygon" not in self.api_keys:
                raise ValueError("使用Polygon数据源需要提供API KEY")
            self.sources["polygon"] = PolygonSource(self.api_keys["polygon"])
            
        # 初始化备用数据源
        if backup_sources:
            for source in backup_sources:
                if source not in self.sources:
                    if source == "yfinance":
                        self.sources[source] = YFinanceSource()
                    elif source == "polygon":
                        if "polygon" in self.api_keys:
                            self.sources[source] = PolygonSource(self.api_keys["polygon"])
        
        self.primary_source = primary_source
        self.backup_sources = backup_sources or []
    
    def _get_cache_path(self, symbol: str, start: str, end: str, interval: str) -> str:
        """生成缓存文件路径"""
        filename = f"{symbol}_{start}_{end}_{interval}.csv"
        return os.path.join(self.cache_dir, filename)
    
    def fetch_data(
        self,
        symbols: List[str],
        start_date: str,
        end_date: Optional[str] = None,
        interval: str = "1d",
        use_cache: bool = True
    ) -> Dict[str, pd.DataFrame]:
        """
        获取股票历史数据
        
        参数:
            symbols (List[str]): 股票代码列表，如 ['AAPL', 'MSFT']
            start_date (str): 开始日期，格式 'YYYY-MM-DD'
            end_date (str, optional): 结束日期，格式 'YYYY-MM-DD'
            interval (str): 数据间隔，默认为日线 '1d'
            use_cache (bool): 是否使用缓存，默认为True
        """
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
            
        data = {}
        for symbol in symbols:
            cache_path = self._get_cache_path(symbol, start_date, end_date, interval)
            
            # 尝试从缓存加载数据
            if use_cache and os.path.exists(cache_path):
                try:
                    df = pd.read_csv(cache_path, index_col=0, parse_dates=True)
                    data[symbol] = df
                    print(f"从缓存加载 {symbol} 的数据")
                    continue
                except Exception as e:
                    print(f"读取缓存文件失败: {e}")
            
            # 尝试从主数据源获取数据
            df = self.sources[self.primary_source].fetch_history(
                symbol, start_date, end_date, interval
            )
            
            # 如果主数据源失败，尝试备用数据源
            if df is None and self.backup_sources:
                for source_name in self.backup_sources:
                    print(f"尝试使用备用数据源 {source_name}")
                    df = self.sources[source_name].fetch_history(
                        symbol, start_date, end_date, interval
                    )
                    if df is not None:
                        break
            
            if df is None:
                print(f"警告: 所有数据源都未能获取到 {symbol} 的数据")
                data[symbol] = None
            else:
                # 保存到缓存
                if use_cache:
                    df.to_csv(cache_path)
                    print(f"数据已缓存到: {cache_path}")
                data[symbol] = df
                
        return data
    
    def fetch_single(
        self,
        symbol: str,
        start_date: str,
        end_date: Optional[str] = None,
        interval: str = "1d",
        use_cache: bool = True
    ) -> Optional[pd.DataFrame]:
        """获取单个股票的历史数据"""
        result = self.fetch_data(
            symbols=[symbol],
            start_date=start_date,
            end_date=end_date,
            interval=interval,
            use_cache=use_cache
        )
        return result.get(symbol)

# 使用示例
if __name__ == "__main__":
    # 从环境变量读取API密钥
    handler = DataHandler(
        primary_source="yfinance",
        backup_sources=["polygon"]
    )
    
    # 获取最近30天的数据
    start = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    end = datetime.now().strftime('%Y-%m-%d')
    
    # 测试单只股票数据获取
    aapl_data = handler.fetch_single('AAPL', start, end)
    if aapl_data is not None:
        print("\nAAPL数据示例:")
        print(aapl_data.head())