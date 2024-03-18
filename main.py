import requests
import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st
import json
import os
from openai import OpenAI
# Function to get current price of a cryptocurrency
def get_current_price(ticker):
    url = f'https://api.coincap.io/v2/assets/{ticker}'
    response = requests.get(url)
    data = response.json()
    if 'data' in data and 'priceUsd' in data['data']:
        return f"Current Price of {ticker}: {data['data']['priceUsd']} USD"
    else:
        return f"Current Price of {ticker} not available"

# Function to convert cryptocurrency to fiat currency
def convert_to_fiat(ticker, amount):
    price = get_current_price(ticker)
    if "not available" in price:
        return price
    else:
        converted_amount = amount * float(price.split(':')[-1].strip().split()[0])
        return f"{amount} {ticker} is equal to {converted_amount} USD"

# Function to convert fiat currency to cryptocurrency
def convert_to_crypto(ticker, amount):
    price = get_current_price(ticker)
    if "not available" in price:
        return price
    else:
        converted_amount = amount / float(price.split(':')[-1].strip().split()[0])
        return f"{amount} USD is equal to {converted_amount} {ticker}"

# Function to get market cap of a cryptocurrency
def get_market_cap(ticker):
    url = f'https://api.coincap.io/v2/assets/{ticker}'
    response = requests.get(url)
    data = response.json()
    if 'data' in data and 'marketCapUsd' in data['data']:
        return f"Market Cap of {ticker}: {data['data']['marketCapUsd']} USD"
    else:
        return f"Market Cap of {ticker} not available"

# Function to get circulating supply of a cryptocurrency
def get_circulating_supply(ticker):
    url = f'https://api.coincap.io/v2/assets/{ticker}'
    response = requests.get(url)
    data = response.json()
    if 'data' in data and 'supply' in data['data']:
        circulating_supply = data['data']['supply']
        return f"Circulating Supply of {ticker}: {circulating_supply}"
    else:
        return f"Circulating Supply of {ticker} not available"

# Function to get total supply of a cryptocurrency
def get_total_supply(ticker):
    url = f'https://api.coincap.io/v2/assets/{ticker}'
    response = requests.get(url)
    data = response.json()
    if 'data' in data and 'maxSupply' in data['data']:
        total_supply = data['data']['maxSupply']
        return f"Total Supply of {ticker}: {total_supply}"
    else:
        return f"Total Supply of {ticker} not available"

# Function to get highest gainers in the market
def get_highest_gainers():
    url = 'https://api.coincap.io/v2/assets'
    response = requests.get(url)
    data = response.json()
    if 'data' in data:
        gainers = [asset['id'] for asset in data['data'][:15]]
        return f"Highest Gainers: {', '.join(gainers)}"
    else:
        return "Highest gainers not available"

# Function to get trending cryptocurrencies
def get_trending_cryptos():
    url = 'https://api.coincap.io/v2/assets'
    response = requests.get(url)
    data = response.json()
    if 'data' in data:
        trending = [asset['id'] for asset in data['data'][:15]]
        return f"Trending Cryptocurrencies: {', '.join(trending)}"
    else:
        return "Trending cryptocurrencies not available"
def get_price_history(ticker, period='1mo'):
    try:
        crypto = yf.Ticker(ticker)
        prices = crypto.history(period=period)
        return prices
    except Exception as e:
        print(f"Error retrieving price history for {ticker}: {e}")
        return None

# Function to plot price history of a cryptocurrency
def plot_price_history(ticker, period='1mo'):
    prices = get_price_history(ticker, period)
    if prices is not None and not prices.empty:
        prices['Close'].plot(figsize=(10, 6))
        plt.title(f"Price History of {ticker}")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('output.png')
        plt.close()
    else:
        print(f"Price history of {ticker} not available")

functions = [
    {
        "name": "get_current_price",
        "description": "Get the current price(in real time) of a cryptocurrency. Uses CoinCap API. (Ticker type: String(example(bitcoin:'bitcoin')))",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Ticker symbol for a coin, for example, 'bitcoin' for Bitcoin",
                },
            },
            "required": ["ticker"]
        }
    },
    {
        "name": "convert_to_fiat",
        "description": "Convert cryptocurrency to fiat currency. Uses CoinCap API. (Ticker type: String(example(bitcoin:'bitcoin')))",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Ticker symbol for a coin, for example, 'bitcoin' for Bitcoin",
                },
                "amount": {
                    "type": "number",
                    "description": "Amount of cryptocurrency to convert to fiat currency",
                }
            },
            "required": ["ticker", "amount"]
        }
    },
    {
        "name": "convert_to_crypto",
        "description": "Convert fiat currency to cryptocurrency. Uses CoinCap API. (Ticker type: String(example(bitcoin:'bitcoin')))",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Ticker symbol for a coin, for example, 'bitcoin' for Bitcoin",
                },
                "amount": {
                    "type": "number",
                    "description": "Amount of fiat currency to convert to cryptocurrency",
                }
            },
            "required": ["ticker", "amount"]
        }
    },
    {
        "name": "get_market_cap",
        "description": "Get the market capitalization of a cryptocurrency((in real time)). Uses CoinCap API. (Ticker type: String(example(bitcoin:'bitcoin')))",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Ticker symbol for a coin, for example, 'bitcoin' for Bitcoin",
                },
            },
            "required": ["ticker"]
        }
    },
    {
        "name": "get_circulating_supply",
        "description": "Get the circulating supply of a cryptocurrency((in real time)). Uses CoinCap API. (Ticker type: String(example(bitcoin:'bitcoin')))",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Ticker symbol for a coin, for example, 'bitcoin' for Bitcoin",
                },
            },
            "required": ["ticker"]
        }
    },
    {
        "name": "get_total_supply",
        "description": "Get the total supply of a cryptocurrency((in real time)). Uses CoinCap API. (Ticker type: String(example(bitcoin:'bitcoin')))",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Ticker symbol for a coin, for example, 'bitcoin' for Bitcoin",
                },
            },
            "required": ["ticker"]
        }
    },
    {
        "name": "get_highest_gainers",
        "description": "Get the highest gainers in the market((in real time)). Uses CoinCap API. (Ticker type: None)"
    },
    {
        "name": "get_trending_cryptos",
        "description": "Get trending cryptocurrencies. Uses CoinCap API. (Ticker type: None)"
    },
    {
        "name": "get_price_history",
        "description": "Get price history of a cryptocurrency. Uses yfinance API. (Ticker type: String(example(bitcoin:'BTC-USD')))",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Ticker symbol for a coin, for example, 'BTC-USD' for Bitcoin",
                },
                "period": {
                    "type": "string",
                    "description": "The period for which historical data should be retrieved (e.g., '1mo' for 1 month, '1d' for 1 day)",
                    "default": "1mo"
                }
            },
            "required": ["ticker"]
        }
    },
    {
        "name": "plot_price_history",
        "description": "Plot price history of a cryptocurrency. Uses yfinance API. (Ticker type: String(example(bitcoin:'BTC-USD')))",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Ticker symbol for a coin, for example, 'BTC-USD' for Bitcoin",
                },
                "period": {
                    "type": "string",
                    "description": "The period for which historical data should be retrieved (e.g., '1mo' for 1 month, '1d' for 1 day)",
                    "default": "1mo"
                }
            },
            "required": ["ticker"]
        }
    }
]

available_functions={
    "get_current_price":get_current_price,
    "convert_to_fiat":convert_to_fiat,
    "convert_to_crypto":convert_to_crypto,
    "get_market_cap":get_market_cap,
    "get_circulating_supply":get_circulating_supply,
    "get_total_supply":get_total_supply,
    "get_highest_gainers":get_highest_gainers,
    "get_trending_cryptos":get_trending_cryptos,
    "get_price_history":get_price_history,
    "plot_price_history":plot_price_history
}
if "messages" not in st.session_state:
    st.session_state["messages"]=[]
st.title("Crypto Currency Chatbot Assistant")
user_input=st.text_input("What's on your mind")
os.environ["OPENAI_API_KEY"] = open('api_openai_key','r').read()
client=OpenAI()
if user_input is not None:
    try:
        st.session_state.messages.append({'role': 'user', 'content': f'{user_input}'})
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=st.session_state.messages,
            functions=functions,
            function_call='auto'
        )
        response_message = response.choices[0].message.content
        response_message = response.choices[0].message
        if response_message:
            if response_message.function_call:
                function_name = response_message.function_call.name
                function_args = json.loads(response_message.function_call.arguments)
                if function_name in ["get_highest_gainers", "get_trending_cryptos"]:
                    args_dict = {}
                elif function_name in ["convert_to_fiat", "convert_to_crypto"]:
                    args_dict = {'ticker': function_args.get('ticker'), 'amount': function_args.get('amount')}
                else:
                    args_dict = {'ticker': function_args.get('ticker')}
                function_to_call = available_functions[function_name]
                function_response = function_to_call(**args_dict)
                if function_name == 'get_price_history':
                    st.table(function_response)
                elif function_name == 'plot_price_history':
                    st.image('output.png')
                else:
                    st.session_state.messages.append(response_message)
                    st.session_state.messages.append(
                        {
                            'role': 'function',
                            'name': function_name,
                            'content': function_response
                        }
                    )
                    second_response = client.chat.completions.create(
                        model='gpt-3.5-turbo',
                        messages=st.session_state.messages
                    )
                    st.text(second_response.choices[0].message.content)
                    st.session_state.messages.append({'role': 'assistant', 'content': response_message.content})
            else:
                st.text(response_message.content)
                st.session_state.messages.append({'role': 'assistant', 'content': response_message.content})
    except Exception as e:
        raise(e)
    
    
