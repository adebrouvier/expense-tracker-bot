class Expense:
    """Expense

    """

    def __init__(self, date, description, location, price, category):
        self.date = date
        self.description = description
        self.location = location
        self.price = price
        self.category = category

    def to_values(self):
        return [self.description, self.location, self.price, self.category]

    def __str__(self):
        return 'Expense: {self.description}, {self.location}, {self.price},' \
            ' {self.category}'.format(self=self)
