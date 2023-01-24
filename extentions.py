import requests
import json
from config import keys, api

API = {'apikey': api}

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}.')

        try:
            base_ticker = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}.')
            
        quote_ticker, base_ticker = keys[quote], keys[base]
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={quote_ticker}&from={base_ticker}&amount={amount}"    
        r = requests.request(\
                "GET", \
                url, \
                headers=API, \
                data={})

        t_base = json.loads(r.content)
        
        return t_base
