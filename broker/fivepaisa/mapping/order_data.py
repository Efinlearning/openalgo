import json
from database.token_db import get_symbol, get_oa_symbol 

def map_order_data(order_data):
    """
    Processes and modifies a list of order dictionaries based on specific conditions.
    
    Parameters:
    - order_data: A list of dictionaries, where each dictionary represents an order.
    
    Returns:
    - The modified order_data with updated 'tradingsymbol' and 'product' fields.
    """
        # Check if 'data' is None
    if order_data['body']['OrderBookDetail'] is None:
        # Handle the case where there is no data
        # For example, you might want to display a message to the user
        # or pass an empty list or dictionary to the template.
        print("No data available.")
        order_data = {}  # or set it to an empty list if it's supposed to be a list
    else:
        order_data = order_data['body']['OrderBookDetail']
        


    if order_data:
        for order in order_data:
            # Extract the instrument_token and exchange for the current order
            symboltoken = order['symboltoken']
            exchange = order['exchange']
            
            # Use the get_symbol function to fetch the symbol from the database
            symbol_from_db = get_symbol(symboltoken, exchange)
            
            # Check if a symbol was found; if so, update the trading_symbol in the current order
            if symbol_from_db:
                order['tradingsymbol'] = symbol_from_db
                if (order['exchange'] == 'NSE' or order['exchange'] == 'BSE') and order['producttype'] == 'DELIVERY':
                    order['producttype'] = 'CNC'
                               
                elif order['producttype'] == 'INTRADAY':
                    order['producttype'] = 'MIS'
                
                elif order['exchange'] in ['NFO', 'MCX', 'BFO', 'CDS'] and order['producttype'] == 'CARRYFORWARD':
                    order['producttype'] = 'NRML'
            else:
                print(f"Symbol not found for token {symboltoken} and exchange {exchange}. Keeping original trading symbol.")
                
    return order_data


def calculate_order_statistics(order_data):
    """
    Calculates statistics from order data, including totals for buy orders, sell orders,
    completed orders, open orders, and rejected orders.

    Parameters:
    - order_data: A list of dictionaries, where each dictionary represents an order.

    Returns:
    - A dictionary containing counts of different types of orders.
    """
    # Initialize counters
    total_buy_orders = total_sell_orders = 0
    total_completed_orders = total_open_orders = total_rejected_orders = 0

    if order_data:
        for order in order_data:
            # Count buy and sell orders
            if order['transactiontype'] == 'BUY':
                total_buy_orders += 1
            elif order['transactiontype'] == 'SELL':
                total_sell_orders += 1
            
            # Count orders based on their status
            if order['status'] == 'complete':
                total_completed_orders += 1
            elif order['status'] == 'open':
                total_open_orders += 1
            elif order['status'] == 'rejected':
                total_rejected_orders += 1

    # Compile and return the statistics
    return {
        'total_buy_orders': total_buy_orders,
        'total_sell_orders': total_sell_orders,
        'total_completed_orders': total_completed_orders,
        'total_open_orders': total_open_orders,
        'total_rejected_orders': total_rejected_orders
    }


def transform_order_data(orders):
    # Directly handling a dictionary assuming it's the structure we expect
    if isinstance(orders, dict):
        # Convert the single dictionary into a list of one dictionary
        orders = [orders]

    transformed_orders = []
    
    for order in orders:
        # Make sure each item is indeed a dictionary
        if not isinstance(order, dict):
            print(f"Warning: Expected a dict, but found a {type(order)}. Skipping this item.")
            continue

        transformed_order = {
            "symbol": order.get("tradingsymbol", ""),
            "exchange": order.get("exchange", ""),
            "action": order.get("transactiontype", ""),
            "quantity": order.get("quantity", 0),
            "price": order.get("price", 0.0),
            "trigger_price": order.get("triggerprice", 0.0),
            "pricetype": order.get("ordertype", ""),
            "product": order.get("producttype", ""),
            "orderid": order.get("orderid", ""),
            "order_status": order.get("status", ""),
            "timestamp": order.get("updatetime", "")
        }

        transformed_orders.append(transformed_order)

    return transformed_orders



def map_trade_data(trade_data):
    """
    Processes and modifies a list of order dictionaries based on specific conditions.
    
    Parameters:
    - order_data: A list of dictionaries, where each dictionary represents an order.
    
    Returns:
    - The modified order_data with updated 'tradingsymbol' and 'product' fields.
    """
        # Check if 'data' is None
    if trade_data['body']['TradeBookDetail'] is None:
        # Handle the case where there is no data
        # For example, you might want to display a message to the user
        # or pass an empty list or dictionary to the template.
        print("No data available.")
        trade_data = {}  # or set it to an empty list if it's supposed to be a list
    else:
        trade_data = trade_data['body']['TradeBookDetail']
        


    if trade_data:
        for order in trade_data:
            # Extract the instrument_token and exchange for the current order
            symbol = order['tradingsymbol']
            exchange = order['exchange']
            
            # Use the get_symbol function to fetch the symbol from the database
            symbol_from_db = get_oa_symbol(symbol, exchange)
            
            # Check if a symbol was found; if so, update the trading_symbol in the current order
            if symbol_from_db:
                order['tradingsymbol'] = symbol_from_db
                if (order['exchange'] == 'NSE' or order['exchange'] == 'BSE') and order['producttype'] == 'DELIVERY':
                    order['producttype'] = 'CNC'
                               
                elif order['producttype'] == 'INTRADAY':
                    order['producttype'] = 'MIS'
                
                elif order['exchange'] in ['NFO', 'MCX', 'BFO', 'CDS'] and order['producttype'] == 'CARRYFORWARD':
                    order['producttype'] = 'NRML'
            else:
                print(f"Unable to find the symbol {symbol} and exchange {exchange}. Keeping original trading symbol.")
                
    return trade_data




def transform_tradebook_data(tradebook_data):
    transformed_data = []
    for trade in tradebook_data:
        transformed_trade = {
            "symbol": trade.get('tradingsymbol', ''),
            "exchange": trade.get('exchange', ''),
            "product": trade.get('producttype', ''),
            "action": trade.get('transactiontype', ''),
            "quantity": trade.get('quantity', 0),
            "average_price": trade.get('fillprice', 0.0),
            "trade_value": trade.get('tradevalue', 0),
            "orderid": trade.get('orderid', ''),
            "timestamp": trade.get('filltime', '')
        }
        transformed_data.append(transformed_trade)
    return transformed_data


def map_position_data(position_data):
    """
    Processes and modifies a list of OpenPosition dictionaries based on specific conditions.
    
    Parameters:
    - position_data: A list of dictionaries, where each dictionary represents an Open Position.
    
    Returns:
    - The modified order_data with updated 'tradingsymbol'
    """
        # Check if 'data' is None
    if position_data['body']['NetPositionDetail'] is None:
        # Handle the case where there is no data
        # For example, you might want to display a message to the user
        # or pass an empty list or dictionary to the template.
        print("No data available.")
        position_data = {}  # or set it to an empty list if it's supposed to be a list
    else:
        position_data = position_data['body']['NetPositionDetail'] 
        
    print(position_data)

    if position_data:
        for position in position_data:
            # Extract the instrument_token and exchange for the current order
            exchange_code = position['exchange']
            segment_code = position['segment']
            exchange = 'get_exchange(exchange_code, segment_code)'
            symbol = position['symbol']
       
            
            # Check if a symbol was found; if so, update the trading_symbol in the current order
            if symbol:
                position['symbol'] = get_oa_symbol(symbol=symbol,exchange=exchange)
                position['exchange'] = exchange
            else:
                print(f"{symbol} and exchange {exchange} not found. Keeping original trading symbol.")
                
    return position_data


def transform_positions_data(positions_data):
    transformed_data = []
    for position in positions_data:
        transformed_position = {
            "symbol": position.get('tradingsymbol', ''),
            "exchange": position.get('exchange', ''),
            "product": position.get('producttype', ''),
            "quantity": position.get('netqty', 0),
            "average_price": position.get('avgnetprice', 0.0),
        }
        transformed_data.append(transformed_position)
    return transformed_data

def transform_holdings_data(holdings_data):
    transformed_data = []
    for holdings in holdings_data['holdings']:
        transformed_position = {
            "symbol": holdings.get('tradingsymbol', ''),
            "exchange": holdings.get('exchange', ''),
            "quantity": holdings.get('quantity', 0),
            "product": holdings.get('product', ''),
            "pnl": holdings.get('profitandloss', 0.0),
            "pnlpercent": holdings.get('pnlpercentage', 0.0)
        }
        transformed_data.append(transformed_position)
    return transformed_data

def map_portfolio_data(portfolio_data):
    """
    Processes and modifies a list of Portfolio dictionaries based on specific conditions and
    ensures both holdings and totalholding parts are transmitted in a single response.
    
    Parameters:
    - portfolio_data: A dictionary, where keys are 'holdings' and 'totalholding',
                      and values are lists/dictionaries representing the portfolio information.
    
    Returns:
    - The modified portfolio_data with 'product' fields changed for 'holdings' and 'totalholding' included.
    """
    # Check if 'data' is None or doesn't contain 'holdings'
    if portfolio_data['body']['Data'] is None:
        print("No data available.")
        # Return an empty structure or handle this scenario as needed
        return {}

    # Directly work with 'data' for clarity and simplicity
    data = portfolio_data['body']['Data']

    # Modify 'product' field for each holding if applicable
    if data.get('holdings'):
        for portfolio in data['holdings']:
            symbol = portfolio['tradingsymbol']
            exchange = portfolio['exchange']
            symbol_from_db = get_oa_symbol(symbol, exchange)
            
            # Check if a symbol was found; if so, update the trading_symbol in the current order
            if symbol_from_db:
                portfolio['tradingsymbol'] = symbol_from_db
            if portfolio['product'] == 'DELIVERY':
                portfolio['product'] = 'CNC'  # Modify 'product' field
            else:
                print("AngelOne Portfolio - Product Value for Delivery Not Found or Changed.")
    
    # The function already works with 'data', which includes 'holdings' and 'totalholding',
    # so we can return 'data' directly without additional modifications.
    return data


def calculate_portfolio_statistics(holdings_data):
    totalholdingvalue = holdings_data['totalholding']['totalholdingvalue']
    totalinvvalue = holdings_data['totalholding']['totalinvvalue']
    totalprofitandloss = holdings_data['totalholding']['totalprofitandloss']
    
    # To avoid division by zero in the case when total_investment_value is 0
    totalpnlpercentage = holdings_data['totalholding']['totalpnlpercentage']

    return {
        'totalholdingvalue': totalholdingvalue,
        'totalinvvalue': totalinvvalue,
        'totalprofitandloss': totalprofitandloss,
        'totalpnlpercentage': totalpnlpercentage
    }


