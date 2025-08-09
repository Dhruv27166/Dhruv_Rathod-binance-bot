"""binance_client.py
Small REST-based Binance USDT-M Futures client for Testnet.
Uses HMAC SHA256 signing for endpoints that require it.
"""
import time
import hmac
import hashlib
import requests
import logging
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

class BinanceFuturesClient:
    def __init__(self, api_key, api_secret, testnet=True, base_url=None, recv_window=5000):
        self.api_key = api_key
        self.api_secret = api_secret.encode('utf-8')
        self.recv_window = recv_window
        if base_url:
            self.base = base_url.rstrip('/')
        else:
            # default Testnet Futures base (USDT-M)
            self.base = 'https://testnet.binancefuture.com' if testnet else 'https://fapi.binance.com'
        self.session = requests.Session()
        self.session.headers.update({
            'X-MBX-APIKEY': self.api_key,
            'Content-Type': 'application/x-www-form-urlencoded'
        })

    def _sign_payload(self, params: dict):
        params['timestamp'] = int(time.time() * 1000)
        params['recvWindow'] = self.recv_window
        query = urlencode(sorted(params.items()))
        signature = hmac.new(self.api_secret, query.encode('utf-8'), hashlib.sha256).hexdigest()
        signed = query + '&signature=' + signature
        return signed

    def _post(self, path, params, signed=True, timeout=10):
        url = self.base + path
        body = self._sign_payload(params) if signed else urlencode(params)
        logger.info("POST %s ? %s", url, body)
        try:
            r = self.session.post(url, data=body, timeout=timeout)
            logger.info("RESPONSE %s %s", r.status_code, r.text)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            logger.exception("POST request failed: %s %s", url, e)
            raise

    def create_order(self, symbol, side, order_type, quantity=None, price=None, time_in_force='GTC', reduce_only=False, close_position=False, **kwargs):
        """Place an order on USDT-M Futures (fapi/v1/order).
        order_type: MARKET or LIMIT or STOP or TAKE_PROFIT market variants per docs.
        side: BUY or SELL
        quantity: required for MARKET/LIMIT
        price: required for LIMIT
        """
        path = '/fapi/v1/order'
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
        }
        if quantity is not None:
            params['quantity'] = float(quantity)
        if price is not None:
            params['price'] = float(price)
        if order_type == 'LIMIT':
            params['timeInForce'] = time_in_force
        # flags
        if reduce_only:
            params['reduceOnly'] = 'true'
        if close_position:
            params['closePosition'] = 'true'
        params.update(kwargs)
        return self._post(path, params, signed=True)

    def get_order(self, symbol, orderId=None, origClientOrderId=None):
        path = '/fapi/v1/order'
        params = {'symbol': symbol}
        if orderId:
            params['orderId'] = orderId
        if origClientOrderId:
            params['origClientOrderId'] = origClientOrderId
        # GET signed
        query = self._sign_payload(params)
        url = self.base + path + '?' + query
        logger.info("GET %s", url)
        r = self.session.get(url)
        logger.info("RESPONSE %s %s", r.status_code, r.text)
        r.raise_for_status()
        return r.json()

if __name__ == '__main__':
    import logging, os
    logging.basicConfig(level=logging.INFO)
    print('This module provides BinanceFuturesClient (no execution here).')
