class DatabaseManager:
    def __init__(self, database_url):
        self.url = database_url

def calculate_discount(price, discount_percentage):
    # Intentional bug snippet for later: missing validation check
    final_price = price - (price * (discount_percentage / 100))
    return final_price