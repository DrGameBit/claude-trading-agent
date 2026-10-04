from __future__ import annotations

from typing import Dict, Iterable, List

import pandas as pd
import yfinance as yf


class MarketDataProvider:
    def __init__(self, interval: str = "1d", period: str = "365d") -> None:
        self.interval = interval
        self.period = period

    def fetch(self, symbols: Iterable[str]) -> Dict[str, pd.DataFrame]:
        results: Dict[str, pd.DataFrame] = {}
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                df = ticker.history(period=self.period, interval=self.interval, auto_adjust=True)
                if df.empty:
                    raise ValueError(f"No data found for {symbol}")
                df = df.rename(columns={"Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"})
                df = df[["open", "high", "low", "close", "volume"]].dropna()
                if df.empty:
                    raise ValueError(f"No valid rows for {symbol}")
                results[symbol] = df
            except Exception as exc:
                print(f"Warning: unable to fetch {symbol}: {exc}")
        return results

    def fetch_single(self, symbol: str) -> pd.DataFrame:
        data = self.fetch([symbol])
        return data.get(symbol, pd.DataFrame())
