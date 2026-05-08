def get_exchange_rate(currency_from: str, currency_to: str) -> str:
    """
    Fetches the current exchange rate between two currencies.
    Args:
        currency_from: The ISO code of the base currency (e.g., USD).
        currency_to: The ISO code of the target currency (e.g., EUR).
    """
    # Mock logic for the exercise
    rates = {
        ("USD", "EUR"): "0.92",
        ("EUR", "USD"): "1.08",
        ("GBP", "USD"): "1.27"
    }
    return rates.get((currency_from.upper(), currency_to.upper()), "Rate not found.")
