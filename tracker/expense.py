from telegram.utils.helpers import escape_markdown


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

    def to_markdown(self):
        return '❗ *Description*: {}\n📍 *Location*: {}\n💰 *Price*: ${}\n🏷 *Category*: {}\n📅 *Date*: {}' \
               .format(self.description, self.location, self.price, self.category, escape_markdown(text=str(self.date), version=2))

    def __str__(self):
        return 'Expense: {self.description}, {self.location}, {self.price},' \
            ' {self.category}'.format(self=self)
