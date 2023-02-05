from datetime import date
from telegram.utils.helpers import escape_markdown


class Expense:
    """Expense

    """

    def __init__(self, spent_at: date, description: str, location: str, price: str, category: str):
        self.spent_at = spent_at
        self.description = description
        self.location = location
        self.price = price
        self.category = category

    def to_values(self):
        return [self.description, self.location, self.price, self.category]

    def to_markdown(self):
        return '❗ *Description*: {}\n📍 *Location*: {}\n💰 *Price*: ${}\n🏷 *Category*: {}\n📅 *Date*: {}' \
               .format(self.escape(self.description), self.escape(self.location),
                       self.escape(str(self.price)), self.escape(self.category),
                       self.escape(str(self.spent_at)))

    def escape(self, text):
        return escape_markdown(text, version=2)

    def __str__(self):
        return 'Expense: {self.description}, {self.location}, {self.price},' \
            ' {self.category}'.format(self=self)
