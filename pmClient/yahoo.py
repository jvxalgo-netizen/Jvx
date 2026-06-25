import requests
import pandas as pd

YAHOO_QUOTE_URL = "https://query1.finance.yahoo.com/v7/finance/quote"
YAHOO_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"


def _ensure_symbol(symbol):
    if not isinstance(symbol, str) or not symbol.strip():
        raise ValueError("symbol must be a non-empty string")
    return symbol.strip()


def _raise_for_status(response):
    if response.status_code >= 400:
        raise requests.HTTPError(
            f"Yahoo Finance request failed with status {response.status_code}: {response.text}"
        )


def fetch_yahoo_quote(symbol):
    """Fetch the latest quote data for a given symbol from Yahoo Finance."""
    symbol = _ensure_symbol(symbol)
    response = requests.get(YAHOO_QUOTE_URL, params={"symbols": symbol}, timeout=10)
    _raise_for_status(response)

    payload = response.json()
    result = payload.get("quoteResponse", {}).get("result", [])
    if not result:
        return {"error": f"Yahoo Finance quote not found for '{symbol}'."}
    return result[0]


def fetch_yahoo_history(symbol, period="1mo", interval="1d"):
    """Fetch historical OHLCV data for a given symbol from Yahoo Finance."""
    symbol = _ensure_symbol(symbol)
    response = requests.get(
        YAHOO_CHART_URL.format(symbol=symbol),
        params={
            "range": period,
            "interval": interval,
            "includePrePost": "false",
            "events": "div,splits"
        },
        timeout=10,
    )
    _raise_for_status(response)

    payload = response.json()
    chart = payload.get("chart", {})
    if chart.get("error"):
        error = chart["error"].get("description", "Yahoo Finance returned an error")
        return {"error": error}

    result = chart.get("result")
    if not result:
        return {"error": f"Yahoo Finance chart result missing for '{symbol}'."}
    result = result[0]

    timestamps = result.get("timestamp")
    quote = result.get("indicators", {}).get("quote", [{}])[0]
    if not timestamps or not quote:
        return {"error": f"Yahoo Finance history not found for '{symbol}'."}

    data = {
        "open": quote.get("open", []),
        "high": quote.get("high", []),
        "low": quote.get("low", []),
        "close": quote.get("close", []),
        "volume": quote.get("volume", []),
    }
    df = pd.DataFrame(data, index=pd.to_datetime(timestamps, unit="s"))
    df.index.name = "datetime"
    return df
