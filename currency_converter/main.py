
import requests
from fastmcp import FastMCP

mcp = FastMCP("MyCurrencyConverter")

@mcp.tool()
def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str
) -> dict:
    """
    Convert currencies using an external exchange-rate API.
    """

    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    from_currency = from_currency.upper().strip()
    to_currency = to_currency.upper().strip()

    if from_currency == to_currency:
        return {
            "amount": amount,
            "from": from_currency,
            "to": to_currency,
            "converted_amount": amount
        }

    url = "https://api.frankfurter.app/latest"

    response = requests.get(
        url,
        params={
            "from": from_currency,
            "to": to_currency
        },
        timeout=10
    )

    response.raise_for_status()
    data = response.json()

    rate = data["rates"][to_currency]

    return {
        "amount": amount,
        "from": from_currency,
        "to": to_currency,
        "exchange_rate": rate,
        "converted_amount": round(amount * rate, 2),
        "rate_date": data["date"]
    }


if __name__ == "__main__":
    mcp.run()
