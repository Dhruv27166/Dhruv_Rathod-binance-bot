# Binance Futures Testnet Trading Bot

A CLI-based Python bot for Binance **USDT-M Futures Testnet** supporting:
- Market Orders
- Limit Orders
- OCO (One-Cancels-the-Other) Orders
- TWAP (Time-Weighted Average Price) Orders

## 📦 Setup

1. **Clone or extract** this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Edit .env and add your Binance Testnet API keys:
	API_KEY=your_testnet_api_key
	API_SECRET=your_testnet_api_secret

4. Register & get keys:
	Sign up at Binance Futures Testnet
	Generate an API Key and Secret with Futures permissions.
	Save them in your .env.

5. Command Usage:
	All scripts automatically:

	i.Load API keys from .env
	ii.Log actions/errors to bot.log

I.Market Order:
	python src/market_orders.py --symbol BTCUSDT --side BUY --quantity 0.002
	python src/market_orders.py --symbol BTCUSDT --side SELL --quantity 0.002

II.Limit Order:
	# BUY Limit (below market)
	python src/limit_orders.py --symbol BTCUSDT --side BUY --quantity 0.002 --price 57000

	# SELL Limit (above market)
	python src/limit_orders.py --symbol BTCUSDT --side SELL --quantity 0.002 --price 59000

III.OCO Order:
	python src/advanced/oco.py --symbol BTCUSDT --side SELL --quantity 0.002 --take-price 59000 --stop-price 57000
	python src/advanced/oco.py --symbol BTCUSDT --side BUY --quantity 0.002 --take-price 57000 --stop-price 59000

IV.TWAP Order:
	# BUY 0.01 BTC in 5 chunks over 30s
	python src/advanced/twap.py --symbol BTCUSDT --side BUY --quantity 0.01 --chunks 5 --interval 6

	# SELL 0.01 BTC in 4 chunks over 40s
	python src/advanced/twap.py --symbol BTCUSDT --side SELL --quantity 0.01 --chunks 4 --interval 10

6. Logs
	All API requests, responses, and errors are logged in:
	bot.log

**NOTES**

Make sure quantity × price ≥ 100 USDT (Binance Futures minimum notional).

Limit and OCO orders must have valid take/stop prices based on current market price.

You can check the current BTCUSDT price with:
python src/utils/check_price.py --symbol BTCUSDT

*License*
This project is for educational purposes only. Use at your own risk on live accounts.




