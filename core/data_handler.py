import yfinance as yf
import pandas as pd
from typing import List, Dict, Optional
import os
from datetime import datetime, timedelta

class DataHandler:
    """数据获取和管理类"""
    
    def __init__(self, cache_dir: str = "data/cache"):
        """
        初始化数据处理器
        
        参数:
            cache_dir (str): 数据缓存目录路径
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_path(self, symbol: str, start: str, end: str, interval: str) -> str:
        """
        生成缓存文件路径
        
        参数:
            symbol (str): 股票代码
            start (str): 开始日期
            end (str): 结束日期
            interval (str): 数据间隔
        """
        filename = f"{symbol}_{start}_{end}_{interval}.csv"
        return os.path.join(self.cache_dir, filename)
    
    def fetch_data(self, 
                  symbols: List[str],
                  start_date: str,
                  end_date: Optional[str] = None,
                  interval: str = "1d",
                  use_cache: bool = True) -> Dict[str, pd.DataFrame]:
        """
        获取股票历史数据
        
        参数:
            symbols (List[str]): 股票代码列表，如 ['AAPL', 'MSFT']
            start_date (str): 开始日期，格式 'YYYY-MM-DD'
            end_date (str, optional): 结束日期，格式 'YYYY-MM-DD'，默认为当前日期
            interval (str): 数据间隔，默认为日线 '1d'
            use_cache (bool): 是否使用缓存，默认为True
            
        返回:
            Dict[str, pd.DataFrame]: 股票数据字典，键为股票代码，值为DataFrame
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
            
            # 从yfinance获取数据
            try:
                print(f"从 yfinance 下载 {symbol} 的数据...")
                df = yf.download(
                    symbol,
                    start=start_date,
                    end=end_date,
                    interval=interval,
                    progress=False
                )
                
                if df.empty:
                    print(f"警告: 未能获取到 {symbol} 的数据")
                    data[symbol] = None
                else:
                    # 保存到缓存
                    if use_cache:
                        df.to_csv(cache_path)
                        print(f"数据已缓存到: {cache_path}")
                    
                    data[symbol] = df
                    
            except Exception as e:
                print(f"获取 {symbol} 数据时出错: {e}")
                data[symbol] = None
                
        return data
    
    def fetch_single(self,
                    symbol: str,
                    start_date: str,
                    end_date: Optional[str] = None,
                    interval: str = "1d",
                    use_cache: bool = True) -> Optional[pd.DataFrame]:
        """
        获取单个股票的历史数据
        
        参数:
            symbol (str): 股票代码
            start_date (str): 开始日期
            end_date (str, optional): 结束日期
            interval (str): 数据间隔
            use_cache (bool): 是否使用缓存
            
        返回:
            Optional[pd.DataFrame]: 股票数据DataFrame，获取失败时返回None
        """
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
    # 创建数据处理器实例
    handler = DataHandler()
    
    # 获取苹果公司最近一年的日线数据
    start = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    end = datetime.now().strftime('%Y-%m-%d')
    
    # 测试单只股票数据获取
    aapl_data = handler.fetch_single('AAPL', start, end)
    if aapl_data is not None:
        print("\nAAPL数据示例:")
        print(aapl_data.head())
    
    # 测试多只股票数据获取
    stocks = ['MSFT', 'GOOGL']
    multi_data = handler.fetch_data(stocks, start, end)
    for symbol, df in multi_data.items():
        if df is not None:
            print(f"\n{symbol}数据示例:")
            print(df.head())