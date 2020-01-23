import unittest
from tracker.expense import Expense


class TestExpense(unittest.TestCase):

    def test_to_values(self):
        expense = Expense('22-1-2020', 'Merienda', 'Café Martinez', '215', 'Comida')
        self.assertEqual(
                        ['Merienda', 'Café Martinez', '215', 'Comida'],
                        expense.to_values()
        )


if __name__ == '__main__':
    unittest.main()
