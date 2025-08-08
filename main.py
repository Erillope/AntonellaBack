import requests # type: ignore
import time
import hashlib
from base64 import b64encode

url = 'https://ccapi-stg.paymentez.com/v2/'

api_key = 'NUVEISTG-EC-SERVER'

secret_key = "Kn9v6ICvoRXQozQG2rK92WtjG6l08a"

def generate_auth_token(api_key: str, secret_key: str) -> str:
    unix_timestamp = str(int(time.time()))
    uniq_token_string = secret_key + unix_timestamp
    uniq_token_hash = hashlib.sha256(uniq_token_string.encode('utf-8')).hexdigest()
    token_string = f'{api_key};{unix_timestamp};{uniq_token_hash}'
    auth_token = b64encode(token_string.encode('utf-8')).decode('utf-8')
    return auth_token

auth_token = generate_auth_token(api_key, secret_key)

headers = {
            'Auth-Token': auth_token,
            'Content-Type': 'application/json'
        }

response = requests.post(
            url + 'card/add/',
            headers=headers,
            json={
                'user': {
                    'id': "499998",
                    'email': "email_ejemplo@gmail.com",
                },
                'card': {
                    "number": "424242424242424",
                    "expiry_month": 1,
                    "expiry_year": 2030,
                    "cvc": "123",
                    "type": "ax",
                }
            },
        )

'''response = requests.get(
            url + 'card/list/',
            headers=headers,
            params={
                'uid': "e1b9e9f2-2704-4c84-9616-9dd9f97ea05e",
            }
)'''
'''
response = requests.post(
            url + 'transaction/debit/',
            headers=headers,
            json={
                'order': {
                    'amount': 112.00,
                    'description': 'Order transaction',
                    'dev_reference': "213111fd-2f2f-49a4-aed5-00552b4108c5",
                    'taxable_amount': 100.00,
                    'tax_percentage': 12.00,
                    'vat': 12.00,
                },
                'user': {
                    'id': "499997",
                    'email': "email_ejemplo@gmail.com"
                },
                "card": {
                    "token": "6506287176048536245"
                }
            }
        )'''
print(response.status_code)
print(response.json())