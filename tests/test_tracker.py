from datetime import date
from tracker.tracker import create_expense


class TestTracker():

    def test_create_expense(self):
        current_date = date.today()
        user_data = {
            "date": current_date,
            "description": "Latte",
            "location": "Starbucks",
            "price": "200",
            "category": "Food"
        }
        expense = create_expense(user_data, current_date)
        assert expense.description == "Latte"
        assert expense.location == "Starbucks"
        assert expense.price == "200"
        assert expense.category == "Food"
