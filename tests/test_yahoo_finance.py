import pytest
import pandas as pd

from pmClient.yahoo import fetch_yahoo_quote, fetch_yahoo_history


class DummyResponse:
    def __init__(self, status_code, json_data, text=""):
        self.status_code = status_code
        self._json = json_data
        self.text = text

    def json(self):
        return self._json


def test_fetch_yahoo_quote_success(mocker):
    response = DummyResponse(
        200,
        {
            "quoteResponse": {
                "result": [
                    {
                        "symbol": "AAPL",
                        "regularMarketPrice": 180.75,
                        "currency": "USD",
                    }
                ]
            }
        },
    )
    mocker.patch("pmClient.yahoo.requests.get", return_value=response)

    quote = fetch_yahoo_quote("AAPL")

    assert quote["symbol"] == "AAPL"
    assert quote["regularMarketPrice"] == 180.75
    assert quote["currency"] == "USD"


def test_fetch_yahoo_quote_not_found(mocker):
    response = DummyResponse(
        200,
        {
            "quoteResponse": {
                "result": []
            }
        },
    )
    mocker.patch("pmClient.yahoo.requests.get", return_value=response)

    quote = fetch_yahoo_quote("UNKNOWN")

    assert quote == {"error": "Yahoo Finance quote not found for 'UNKNOWN'."}


def test_fetch_yahoo_quote_invalid_symbol():
    with pytest.raises(ValueError):
        fetch_yahoo_quote("")


def test_fetch_yahoo_history_success(mocker):
    response = DummyResponse(
        200,
        {
            "chart": {
                "result": [
                    {
                        "timestamp": [1710000000, 1710086400],
                        "indicators": {
                            "quote": [
                                {
                                    "open": [150.0, 152.0],
                                    "high": [151.0, 153.0],
                                    "low": [149.0, 151.0],
                                    "close": [150.5, 152.5],
                                    "volume": [1000000, 1200000],
                                }
                            ]
                        },
                    }
                ]
            }
        },
    )
    mocker.patch("pmClient.yahoo.requests.get", return_value=response)

    df = fetch_yahoo_history("AAPL", period="2d", interval="1d")

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
    assert df.shape == (2, 5)
    assert df.index.name == "datetime"
    assert df.iloc[0]["open"] == 150.0


def test_fetch_yahoo_history_invalid_symbol():
    with pytest.raises(ValueError):
        fetch_yahoo_history("")
