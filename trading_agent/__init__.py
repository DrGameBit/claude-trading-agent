from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import pandas as pd

from .config import AgentSettings
from .data import MarketDataProvider
from .portfolio import Portfolio
from .risk import RiskManager
from .strategy import Strategy


@dataclass
class TradingAgent:
    settings: AgentSettings
    data_provider: MarketDataProvider
    strategy: Strategy
    risk_manager: RiskManager

    def __init__(self, settings: AgentSettings | None = None) -> None:
        self.settings = settings or AgentSettings()
        self.data_provider = MarketDataProvider(interval=self.settings.interval, period=self.settings.period)
        self.strategy = Strategy(
            buy_threshold=self.settings.buy_threshold,
            sell_threshold=self.settings.sell_threshold,
        )
        self.risk_manager = RiskManager(
            max_position_weight=self.settings.max_position_weight,
            min_risk_budget=self.settings.min_risk_budget,
            risk_per_trade=self.settings.risk_per_trade,
            stop_loss_pct=self.settings.stop_loss_pct,
            take_profit_pct=self.settings.take_profit_pct,
        )

    def run_cycle(self) -> Dict[str, object]:
        market_data = self.data_provider.fetch(self.settings.symbols)
        signals = {}
        prices = {}
        for symbol, df in market_data.items():
            signal = self.strategy.generate_signal(symbol, df)
            signals[symbol] = signal
            prices[symbol] = float(df["close"].iloc[-1])

        portfolio = Portfolio(cash=self.settings.cash)
        for symbol, signal in signals.items():
            if signal.action == "BUY":
                trade_size = self.risk_manager.calculate_trade_size(portfolio.market_value(prices), signal.confidence)
                if trade_size <= 0:
                    continue
                if trade_size > portfolio.cash:
                    trade_size = portfolio.cash
                portfolio.buy(symbol, trade_size, prices[symbol])
            elif signal.action == "SELL":
                if symbol in portfolio.positions:
                    portfolio.sell(symbol, portfolio.positions[symbol].quantity, prices[symbol])

        return {
            "signals": signals,
            "prices": prices,
            "portfolio": portfolio,
            "total_value": portfolio.market_value(prices),
        }

    def snapshot(self) -> List[Dict[str, object]]:
        cycle = self.run_cycle()
        records = []
        for symbol, signal in cycle["signals"].items():
            records.append({
                "symbol": symbol,
                "action": signal.action,
                "score": signal.score,
                "confidence": signal.confidence,
                "reason": signal.reason,
                "price": cycle["prices"][symbol],
            })
        return records
