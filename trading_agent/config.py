from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class AgentSettings:
    symbols: List[str] = field(default_factory=lambda: ["SPY", "QQQ", "BTC-USD", "ETH-USD"])
    interval: str = "1d"
    period: str = "365d"
    cash: float = 100000.0
    max_position_weight: float = 0.25
    min_risk_budget: float = 0.02
    stop_loss_pct: float = 0.12
    take_profit_pct: float = 0.2
    risk_per_trade: float = 0.01
    buy_threshold: float = 0.6
    sell_threshold: float = -0.6


DEFAULT_SETTINGS = AgentSettings()
