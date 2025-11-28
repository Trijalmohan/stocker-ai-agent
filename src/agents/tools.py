from src.database.portfolio import add_or_update_position, sell_position, get_positions
from src.services.market_data import get_stock_price

tools = [
    {
        "name": "get_price",
        "description": "Fetch latest stock price",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string"}
            },
            "required": ["symbol"]
        },
        "function": lambda args: get_stock_price(args["symbol"])
    },
    {
        "name": "buy_stock",
        "description": "Simulate buying shares",
        "input_schema": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string"},
                "qty": {"type": "number"},
                "price": {"type": "number"}
            },
            "required": ["symbol", "qty", "price"]
        },
        "function": lambda args: add_or_update_position(
            args["symbol"], args["qty"], args["price"]
        )
    },
    {
        "name": "get_portfolio",
        "description": "Get full portfolio state",
        "input_schema": {"type": "object", "properties": {}},
        "function": lambda args: get_positions()
    }
]
