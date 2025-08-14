# src/advanced/oco.py
import argparse
import time
import logging
from config import API_KEY, API_SECRET
from common_client import make_futures_client

logging.basicConfig(filename='../../bot.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

def parse_args():
    p = argparse.ArgumentParser(description='Simulated OCO on Futures Testnet')
    p.add_argument('--symbol', required=True)
    p.add_argument('--side', required=True, choices=['BUY','SELL'])
    p.add_argument('--quantity', required=True, type=float)
    p.add_argument('--take-price', required=True, type=float)
    p.add_argument('--stop-price', required=True, type=float)
    p.add_argument('--poll-interval', type=float, default=2.0)
    return p.parse_args()

def main():
    args = parse_args()
    client = make_futures_client(API_KEY, API_SECRET)
    # Place TP (limit) and Stop (stopMarket)
    tp_side = 'SELL' if args.side == 'BUY' else 'BUY'
    try:
        tp = client.futures_create_order(
            symbol=args.symbol, side=tp_side, type='LIMIT', quantity=args.quantity,
            price=str(args.take_price), timeInForce='GTC'
        )
        stop = client.futures_create_order(
            symbol=args.symbol, side=tp_side, type='STOP_MARKET', quantity=args.quantity,
            stopPrice=str(args.stop_price)
        )
        tp_id = tp.get('orderId')
        stop_id = stop.get('orderId')
        print("TP id", tp_id, "STOP id", stop_id)
        logger.info("Placed TP %s and STOP %s", tp, stop)
        while True:
            time.sleep(args.poll_interval)
            tp_status = client.futures_get_order(symbol=args.symbol, orderId=tp_id)
            stop_status = client.futures_get_order(symbol=args.symbol, orderId=stop_id)
            logger.info("TP status: %s", tp_status)
            logger.info("Stop status: %s", stop_status)
            if tp_status.get('status') == 'FILLED':
                # cancel stop
                client.futures_cancel_order(symbol=args.symbol, orderId=stop_id)
                print('Take-profit filled, stop canceled')
                break
            if stop_status.get('status') == 'FILLED':
                client.futures_cancel_order(symbol=args.symbol, orderId=tp_id)
                print('Stop executed, TP canceled')
                break
    except Exception as e:
        logger.exception("OCO simulation failed")
        print("Error:", e)

if __name__ == "__main__":
    main()
