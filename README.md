# Claude Trading Agent

A modular Python trading agent designed for stocks, crypto, and ETFs. It includes:

- market data ingestion for multiple asset classes
- technical indicator-based signal generation
- risk-managed portfolio sizing
- paper trading and backtesting utilities
- a CLI for running analysis on live/market snapshots

This project is a solid starter for building a production trading system and can be extended with broker integration, ML models, and event-driven execution.

## Features

- Multi-asset support: stocks, ETFs, crypto
- Yahoo Finance-backed data pipeline
- Momentum/trend signal engine using SMA, RSI, MACD-style logic
- Position sizing and risk controls
- Paper portfolio simulation
- Backtesting over historical data
- Simple command-line interface

## Quick start

### 1) Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Run the agent

```bash
python -m trading_agent.cli --symbols SPY QQQ AAPL BTC-USD ETH-USD --days 365 --interval 1d
```

### 4) Run a backtest

```bash
python -m trading_agent.cli --symbols SPY BTC-USD --days 365 --interval 1d --backtest
```

## Project structure

```text
trading_agent/
  __init__.py
  agent.py
  backtest.py
  cli.py
  config.py
  data.py
  portfolio.py
  risk.py
  strategy.py
```

## Notes

- This repository is intended for research and educational use.
- It does not provide financial advice or a live-execution broker integration.
- For production trading, add authentication, order validation, slippage modeling, and exchange-specific APIs.

## License

MIT
