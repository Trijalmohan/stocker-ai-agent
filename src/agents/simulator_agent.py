from src.database.portfolio import add_or_update_position, get_positions

class SimulatorAgent:
    def buy(self, symbol: str, qty: float, price: float = 100.0):
        add_or_update_position(symbol, qty, price)
        return {
            "status": "success",
            "message": "Position updated",
            "symbol": symbol,
            "quantity_added": qty,
            "price": price
        }
    def portfolio(self):
        return get_positions()
