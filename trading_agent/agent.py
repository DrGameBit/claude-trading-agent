from __future__ import annotations

from typing import Dict, Iterable

import pandas as pd

from .data import MarketDataProvider
from .portfolio import Portfolio
from .risk import RiskManager
from .strategy import Strategy


class BacktestEngine:
    def __init__(self, strategy: Strategy, risk_manager: RiskManager) -> None:
        self.strategy = strategy
        self.risk_manager = risk_manager

    def run(self, data: Dict[str, pd.DataFrame], initial_cash: float = 100000.0) -> Dict[str, float]:
        portfolio = Portfolio(cash=initial_cash)
        equity_curve = []

        for symbol, df in data.items():
            if df.empty:
                continue
            signal = self.strategy.generate_signal(symbol, df)
            price = float(df["close"].iloc[-1])
            if signal.action == "BUY":
                trade_size = self.risk_manager.calculate_trade_size(initial_cash, signal.confidence)
                portfolio.buy(symbol, min(trade_size, portfolio.cash), price)
            elif signal.action == "SELL":
                if symbol in portfolio.positions:
                    portfolio.sell(symbol, portfolio.positions[symbol].quantity, price)
            equity_curve.append(portfolio.market_value({symbol: price}))

        results = {
            "final_cash": portfolio.cash,
            "final_positions": portfolio.positions,
            "equity_curve": equity_curve,
            "final_value": portfolio.market_value({symbol: df["close"].iloc[-1] for symbol, df in data.items()}),
        }
        return results
