from typing import Dict, List, Optional, Union
import pandas as pd
import numpy as np
import vectorbt as vbt

class BacktestEngine:
    """回测引擎：专注于执行回测和计算回测指标"""
    
    def __init__(
        self,
        initial_capital: float = 100000.0,
        commission: float = 0.001,
        slippage: float = 0.001
    ):
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        
    def run(
        self,
        signals: Dict[str, pd.DataFrame],
        prices: Dict[str, pd.DataFrame]
    ) -> Dict[str, Dict]:
        """执行回测并返回结果"""
        portfolio_results = {}
        
        for symbol, signal_df in signals.items():
            price_df = prices[symbol]
            
            # 创建投资组合
            portfolio = vbt.Portfolio.from_signals(
                close=price_df['Close'],
                entries=signal_df['signal'] == 1,
                exits=signal_df['signal'] == -1,
                init_cash=self.initial_capital,
                fees=self.commission,
                slippage=self.slippage
            )
            
            # 确保所有数据具有相同的索引
            cash = portfolio.cash()
            value = portfolio.value()
            returns = portfolio.returns()
            drawdown = portfolio.drawdown()
            
            # 创建每日投资组合状态
            daily_stats = pd.DataFrame(index=price_df.index)
            daily_stats['Close'] = price_df['Close']
            daily_stats['Position'] = portfolio.positions.values
            daily_stats['Cash'] = cash
            daily_stats['Holdings'] = value
            daily_stats['Total_Value'] = value + cash
            daily_stats['Returns'] = returns
            daily_stats['Drawdown'] = drawdown
            
            # 计算交易统计
            trade_stats = {
                'total_trades': len(portfolio.trades),
                'win_rate': portfolio.win_rate(),
                'avg_win': portfolio.trades.winning.pnl.mean() if len(portfolio.trades.winning) > 0 else 0,
                'avg_loss': portfolio.trades.losing.pnl.mean() if len(portfolio.trades.losing) > 0 else 0,
                'max_win': portfolio.trades.winning.pnl.max() if len(portfolio.trades.winning) > 0 else 0,
                'max_loss': portfolio.trades.losing.pnl.min() if len(portfolio.trades.losing) > 0 else 0,
                'avg_hold_time': portfolio.trades.duration.mean() if len(portfolio.trades) > 0 else 0
            }
            
            # 计算风险指标
            risk_metrics = {
                'total_return': portfolio.total_return(),
                'sharpe_ratio': portfolio.sharpe_ratio(),
                'sortino_ratio': portfolio.sortino_ratio(),
                'calmar_ratio': portfolio.calmar_ratio(),
                'max_drawdown': portfolio.max_drawdown(),
                'annual_return': portfolio.annual_return(),
                'annual_volatility': portfolio.annual_volatility()
            }
            
            portfolio_results[symbol] = {
                'daily_stats': daily_stats,
                'trade_stats': trade_stats,
                'risk_metrics': risk_metrics,
                'trades': portfolio.trades.records_readable
            }
            
        return portfolio_results