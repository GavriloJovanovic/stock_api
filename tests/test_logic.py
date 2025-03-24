# tests/test_logic.py

import pytest
import pandas as pd
from datetime import datetime
from app.logic import StockLogic

import pandas as pd
from datetime import datetime

from app.logic import StockLogic

@pytest.fixture
def mock_data():
    data = [
        {"date": datetime(2020, 6, 1).date(), "close": 100},
        {"date": datetime(2020, 6, 2).date(), "close": 105},
        {"date": datetime(2020, 6, 3).date(), "close": 102},
        {"date": datetime(2020, 6, 4).date(), "close": 110},
        {"date": datetime(2020, 6, 5).date(), "close": 108}
    ]
    return pd.DataFrame(data)

def test_get_best_trade(mock_data):
    result = StockLogic.get_best_trade(mock_data, datetime(2020, 6, 1).date(), datetime(2020, 6, 5).date())

    assert result["buy_date"] == "2020-06-01"
    assert result["sell_date"] == "2020-06-04"
    assert result["profit"] == 10.0
    assert result["buy_price"] == 100.0
    assert result["sell_price"] == 110.0

def test_get_total_profit(mock_data):
    result = StockLogic.get_total_profit(mock_data, datetime(2020, 6, 1).date(), datetime(2020, 6, 5).date())

    # profit: 100 -> 105 = 5, 102 -> 110 = 8 (we are counting the prices when it is growing in regard to previous day)
    assert result == 13.0