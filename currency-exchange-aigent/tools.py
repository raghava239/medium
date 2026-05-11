import os
import requests

def get_live_exchange_rates(base_currency: str) -> dict:
    """Fetches real-time exchange rates using a secure API Key."""
    # We pull the key from the environment instead of hardcoding it
    api_key = os.environ.get("EXCHANGE_RATE_API_KEY")
    
    if not api_key:
        return {"error": "API Key not configured in environment."}

    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency.upper()}"
    
    try:
        response = requests.get(url)
        data = response.json()
        return data.get("conversion_rates", {"error": "Invalid response"})
    except Exception as e:
        return {"error": str(e)}
