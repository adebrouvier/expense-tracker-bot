from tracker.expense import Expense


class TestExpense():

    def test_to_values(self):
        expense = Expense('22-1-2020', 'Merienda', 'Café Martinez', '215', 'Comida')
        assert ['Merienda', 'Café Martinez', '215', 'Comida'] == expense.to_values()
