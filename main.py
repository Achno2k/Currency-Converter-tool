import json
from requests import get
from pprint import PrettyPrinter

def read_api_key(file_path='config.json'):
    try:
        with open(file_path, 'r') as config_file:
            config_data = json.load(config_file)
            api_key = config_data.get('api_key')
            if api_key:
                return api_key
            else:
                raise ValueError('API key not found in the configuration file.')
    except FileNotFoundError:
        raise FileNotFoundError(f'Configuration file not found: {file_path}')
    except json.JSONDecodeError:
        raise ValueError(f'Error decoding JSON in configuration file: {file_path}')
    
BASE_URL = "https://free.currconv.com/"
API_KEY = read_api_key()


printer = PrettyPrinter()

def get_currencies():
    endpoint = f"api/v7/currencies?apiKey={API_KEY}"
    url = BASE_URL + endpoint
    data = get(url).json()['results']

    data = list(data.items())
    data.sort()

    return data


def print_currencies(currencies):
    for name, currency in currencies:
        name = currency['currencyName']
        _id = currency['id']
        symbol = currency.get("currencySymbol", "")
        print(f"{_id} - {name} - {symbol}")


def exchange_rate(currency1, currency2):
    endpoint = f"api/v7/convert?q={currency1}_{currency2}&compact=ultra&apiKey={API_KEY}"
    url = BASE_URL + endpoint
    data = get(url).json()

    if len(data) == 0:
        print('Invalid currencies.')
        return

    rate = list(data.values())[0]
    print(f"{currency1} -> {currency2} = {rate}")

    return rate


def convert(currency1, currency2, amount):
    rate = exchange_rate(currency1, currency2)
    if rate is None:
        return

    try:
        amount = float(amount)
    except:
        print("Invalid amount.")
        return

    converted_amount = rate * amount
    print(f"{amount} {currency1} is equal to {round(converted_amount,3)} {currency2}")
    return converted_amount

def validate_currency(input_currency):
    currencyList = []
    for name, currency in currencies:
        _id = currency['id']
        currencyList.append(_id)
    
    if input_currency in currencyList:
        return True
    else:
        return False
    

def main():

    print("===============================================")
    print("WELCOME TO CURRENCY CONVERTOR!")
    print("Commands are listed below.")
    print("--> List - lists the different currencies")
    print("--> Convert - convert from one currency to another")
    print("--> Rate - get the exchange rate of two currencies")
    print("===============================================")
    print()

    while True:
        print()
        command = input("Enter a command (q to quit): ").lower()

        if command == "q":
            print()
            print('Thank you for using the currency converter. Goodbye!')
            break
        elif command == "list":
            print_currencies(currencies)
        elif command == "convert":
            currency1 = input("Enter a base currency: ").upper()
            currency2 = input("Enter a currency to convert to: ").upper()
            
            if (validate_currency(currency1) and validate_currency(currency2)):
                amount = input(f"Enter an amount in {currency1}: ")
                convert(currency1, currency2, amount)
            else:
                print("Invalid currency code.")
                continue
        elif command == "rate":
            currency1 = input("Enter a base currency: ").upper()
            currency2 = input("Enter a currency to convert to: ").upper()
            exchange_rate(currency1, currency2)
        else:
            print("Unrecognized command!")
            
if __name__ == '__main__':
    currencies = get_currencies()
    main()
    
