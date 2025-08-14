# src/advanced/twap.py
import argparse
import time
import logging
from config import API_KEY, API_SECRET
from common_client import make_futures_client

logging.basicConfig(filename='../../bot.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

def parse_args():
    p = argparse.ArgumentParser(description='Basic TWAP on Futures Testnet')
    p.add_argument('--symbol', required=True)
    p.add_argument('--side', required=True, choices=['BUY','SELL'])
    p.add_argument('--total-qty', required=True, type=float)
    p.add_argument('--slices', type=int, default=5)
    p.add_argument('--duration', type=float, default=60.0, help='seconds')
    return p.parse_args()

def main():
    args = parse_args()
    client = make_futures_client(API_KEY, API_SECRET)
    qty_per = args.total_qty / args.slices
    wait = args.duration / args.slices
    for i in range(args.slices):
        try:
            resp = client.futures_create_order(
                symbol=args.symbol, side=args.side, type='MARKET', quantity=qty_per
            )
            logger.info("TWAP slice %s: %s", i+1, resp)
            print(f"Slice {i+1} response:", resp)
        except Exception as e:
            logger.exception("TWAP slice failed")
            print("Error on slice", i+1, e)
        time.sleep(wait)

if __name__ == "__main__":
    main()
