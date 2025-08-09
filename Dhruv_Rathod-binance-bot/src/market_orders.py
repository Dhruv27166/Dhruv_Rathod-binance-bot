# src/market_orders.py
import argparse
import logging
from config import API_KEY, API_SECRET
from common_client import make_futures_client
# Setup logging to file
logging.basicConfig(filename='../bot.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

def parse_args():
    p = argparse.ArgumentParser(description='Place a MARKET order on Binance Futures Testnet')
    p.add_argument('--symbol', required=True, help='e.g. BTCUSDT')
    p.add_argument('--side', required=True, choices=['BUY', 'SELL'])
    p.add_argument('--quantity', required=True, type=float)
    return p.parse_args()

def main():
    args = parse_args()
    client = make_futures_client(API_KEY, API_SECRET)
    try:
        resp = client.futures_create_order(
            symbol=args.symbol,
            side=args.side,
            type='MARKET',
            quantity=args.quantity
        )
        print("Order response:")
        print(resp)
        logger.info("Placed MARKET order: %s", resp)
    except Exception as e:
        logger.exception("Failed to place market order")
        print("Error:", e)

if __name__ == "__main__":
    main()
