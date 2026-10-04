from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Position:
    symbol: str
    quantity: float
    entry_price: float
    value: float


@dataclass
class Portfolio:
    cash: float
    positions: Dict[str, Position] = field(default_factory=dict)

    def market_value(self, price_map: Dict[str, float]) -> float:
        total = self.cash
        for symbol, position in self.positions.items():
            total += position.quantity * price_map.get(symbol, position.entry_price)
        return total

    def buy(self, symbol: str, cash_to_allocate: float, current_price: float) -> None:
        quantity = cash_to_allocate / current_price
        if quantity <= 0:
            return
        if symbol in self.positions:
            existing = self.positions[symbol]
            existing.quantity += quantity
            existing.entry_price = (existing.entry_price * existing.quantity + current_price * quantity) / (existing.quantity + quantity)
            existing.value = existing.quantity * current_price
        else:
            self.positions[symbol] = Position(symbol=symbol, quantity=quantity, entry_price=current_price, value=current_price * quantity)
        self.cash -= cash_to_allocate

    def sell(self, symbol: str, quantity: float, current_price: float) -> None:
        if symbol not in self.positions:
            return
        position = self.positions[symbol]
        sell_quantity = min(quantity, position.quantity)
        if sell_quantity <= 0:
            return
        position.quantity -= sell_quantity
        self.cash += sell_quantity * current_price
        if position.quantity <= 0:
            del self.positions[symbol]

    def rebalance(self, signal_map: Dict[str, object], price_map: Dict[str, float], risk_manager: object) -> None:
        for symbol, signal in signal_map.items():
            if signal.action == "BUY":
                trade_size = risk_manager.calculate_trade_size(self.market_value(price_map), signal.confidence)
                if trade_size > self.cash:
                    trade_size = self.cash
                if trade_size > 0:
                    self.buy(symbol, trade_size, price_map.get(symbol, 0.0))
            elif signal.action == "SELL":
                if symbol in self.positions:
                    self.sell(symbol, self.positions[symbol].quantity, price_map.get(symbol, 0.0))
