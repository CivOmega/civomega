import json
import re
import unittest

from civomega.modules.test_campaign_finance import (ContributorParser,
        MoneyRaisedParser, AWESOME_DATABASE)


class TestContributorParser(unittest.TestCase):
    def setUp(self):
        self.matcher = ContributorParser()

    def test_can_find_contributors_for_perry(self):
        result = self.matcher.search("Who gave money to Rick Perry")
        data = result.as_json()
        self.assert_("Texans for Perry" in json.loads(data))
        self.assert_("Texans who are really for Perry" in json.loads(data))

    def test_can_find_contributors_for_dewhurst(self):
        result = self.matcher.search("Who gave money to David Dewhurst")
        data = result.as_json()
        self.assert_("Texans for Dewhurst" in json.loads(data))
        self.assert_("Texans who are really for Dewhurst" in json.loads(data))

    def test_returns_none_for_nothing(self):
        result = self.matcher.search("Who did not give money to Rick Perry")
        self.assert_(result is None)


class TestMoneyRaisedParser(unittest.TestCase):
    def setUp(self):
        self.matcher = MoneyRaisedParser()

    def test_can_find_money_raised_for_perry(self):
        result = self.matcher.search("How much money has Rick Perry raised")
        data = json.loads(result.as_json())
        self.assert_(AWESOME_DATABASE['Rick Perry']['total_money_raised'] == data["raised"])

    def test_can_find_money_raised_for_dewhurst(self):
        result = self.matcher.search("How much money has David Dewhurst raised")
        data = json.loads(result.as_json())
        self.assert_(AWESOME_DATABASE['David Dewhurst']['total_money_raised'] == data["raised"])

    def test_returns_none_for_no_match(self):
        result = self.matcher.search("How much money didn't Rick Perry raise")
        self.assert_(result is None)
