# src/common_client.py
from binance.client import Client
import logging

TESTNET_FUTURES_API = 'https://testnet.binancefuture.com/fapi'

logger = logging.getLogger(__name__)

def make_futures_client(api_key, api_secret):
    """
    Returns a python-binance Client configured for USDT-M Futures Testnet.
    """
    client = Client(api_key, api_secret, testnet=True)
    # Ensure futures endpoints point to the Testnet futures base
    # The python-binance package stores API_URL used by some methods; set both if available
    try:
        client.API_URL = TESTNET_FUTURES_API
    except Exception:
        logger.debug("client.API_URL not settable on this python-binance version")
    return client
