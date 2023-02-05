from tracker.expense import Expense


class TestExpense():

    def test_to_values(self):
        expense = Expense('22-1-2020', 'Merienda', 'Café Martinez', '215', 'Comida')
        assert ['Merienda', 'Café Martinez', '215', 'Comida'] == expense.to_values()

    def test_to_markdown(self):
        expense = Expense('22-1-2020', 'Merienda', 'Café Martinez', '215', 'Comida')
        expected_markdown = '❗ *Description*: Merienda\n📍 *Location*: Café Martinez\n' \
                            + '💰 *Price*: $215\n🏷 *Category*: Comida\n📅 *Date*: 22\\-1\\-2020'
        assert expected_markdown == expense.to_markdown()
