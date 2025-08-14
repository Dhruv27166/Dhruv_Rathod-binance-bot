# src/limit_orders.py
import argparse
import logging
from config import API_KEY, API_SECRET
from common_client import make_futures_client
logging.basicConfig(filename='../bot.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

def parse_args():
    p = argparse.ArgumentParser(description='Place a LIMIT order on Binance Futures Testnet')
    p.add_argument('--symbol', required=True, help='e.g. BTCUSDT')
    p.add_argument('--side', required=True, choices=['BUY', 'SELL'])
    p.add_argument('--quantity', required=True, type=float)
    p.add_argument('--price', required=True, type=float)
    p.add_argument('--time-in-force', default='GTC', choices=['GTC','IOC','FOK'])
    return p.parse_args()

def main():
    args = parse_args()
    client = make_futures_client(API_KEY, API_SECRET)
    try:
        resp = client.futures_create_order(
            symbol=args.symbol,
            side=args.side,
            type='LIMIT',
            quantity=args.quantity,
            price=str(args.price),     # API expects string/decimal format
            timeInForce=args.time_in_force
        )
        print("Order response:")
        print(resp)
        logger.info("Placed LIMIT order: %s", resp)
    except Exception as e:
        logger.exception("Failed to place limit order")
        print("Error:", e)

if __name__ == "__main__":
    main()
