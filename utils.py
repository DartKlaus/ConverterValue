import requests
import json
from config import API_key, keys


class ConvertionException(Exception):
    pass


class ValueConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException(f'Невозможно конвертировать одинаковые валюты!'
                                      f' Введите еще одну валюту, кроме {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}!')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://api.freecurrencyapi.com/v1/latest?apikey={API_key}'
                         f'&currencies={base_ticker}&base_currency={quote_ticker}')
        total_base = json.loads(r.content)['data'][keys[base]]

        return total_base
