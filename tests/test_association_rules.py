import unittest

import pandas as pd
from mlxtend.frequent_patterns import apriori, fpmax

from scripts.chuandoantrenluat import find_closed_frequent_itemsets


class AssociationItemsetsTest(unittest.TestCase):
    def test_extracts_closed_and_maximal_itemsets_by_definition(self):
        transactions = pd.DataFrame(
            [
                {"A": True, "B": True, "C": False},
                {"A": True, "B": True, "C": False},
                {"A": True, "B": False, "C": True},
            ]
        )

        frequent = apriori(transactions, min_support=0.6, use_colnames=True)
        closed = find_closed_frequent_itemsets(frequent, len(transactions))
        maximal = fpmax(transactions, min_support=0.6, use_colnames=True)

        self.assertEqual(
            set(closed["itemsets"]),
            {frozenset({"A"}), frozenset({"A", "B"})},
        )
        self.assertEqual(set(maximal["itemsets"]), {frozenset({"A", "B"})})


if __name__ == "__main__":
    unittest.main()
