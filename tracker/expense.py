class Expense:
    """Expense

    """

    def __init__(self, date, description, place, price, category):
        self.date = date
        self.description = description
        self.place = place
        self.price = price
        self.category = category

    def to_values(self):
        return [self.description, self.place, self.price, self.category]

    def __str__(self):
        return 'Expense: {self.description}, {self.place}, {self.price}, \
            {self.category}'.format(self=self)
