from datetime import date
from tracker.bot import create_expense
import pytest


class TestTracker():

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_create_expense(self):
        current_date = date(2019, 4, 13)
        user_data = {
            "date": current_date,
            "description": "Latte",
            "location": "Starbucks",
            "price": "200",
            "category": "Food"
        }
        expense = create_expense(user_data, current_date)
        assert expense.date == current_date
        assert expense.description == "Latte"
        assert expense.location == "Starbucks"
        assert expense.price == "200"
        assert expense.category == "Food"
