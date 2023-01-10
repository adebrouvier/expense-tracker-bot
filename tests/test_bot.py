import re
from tracker.bot import price_regex


class TestBot():

    def test_price_regex(self):
        sent_price = "1500"
        match = re.search(price_regex(), sent_price)
        assert match.group(0) == "1500"

    def test_price_regex_does_not_make_partial_match(self):
        sent_price = "1500ab200"
        match = re.search(price_regex(), sent_price)
        assert match is None
