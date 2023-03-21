import unittest

from storage import InMemoryDB


class TestInMemoryDB(unittest.TestCase):
    def setUp(self) -> None:
        self.db = InMemoryDB()

    def test_example_1(self):
        """Example #1 from prompt"""
        self.assertEqual(self.db.get("a"), "NULL")
        self.db.set("a", "foo")
        self.db.set("b", "foo")
        self.assertEqual(self.db.count("foo"), 2)
        self.assertEqual(self.db.count("bar"), 0)
        self.db.delete("a")
        self.assertEqual(self.db.count("foo"), 1)
        self.db.set("b", "baz")
        self.assertEqual(self.db.count("foo"), 0)
        self.assertEqual(self.db.get("b"), "baz")
        self.assertEqual(self.db.get("B"), "NULL")

    def test_example_2(self):
        """Example #2 from prompt"""
        self.db.set("a", "foo")
        self.db.set("a", "foo")
        self.assertEqual(self.db.count("foo"), 1)
        self.assertEqual(self.db.get("a"), "foo")
        self.db.delete("a")
        self.assertEqual(self.db.get("a"), "NULL")
        self.assertEqual(self.db.count("foo"), 0)

    def test_example_3(self):
        """Example #3 from prompt"""
        self.db.begin()
        self.db.set("a", "foo")
        self.assertEqual(self.db.get("a"), "foo")
        self.db.begin()
        self.db.set("a", "bar")
        self.assertEqual(self.db.get("a"), "bar")
        self.db.set("a", "baz")
        self.db.rollback()
        self.assertEqual(self.db.get("a"), "foo")
        self.db.rollback()
        self.assertEqual(self.db.get("a"), "NULL")

    def test_example_4(self):
        """Example #4 from prompt"""
        self.db.set("a", "foo")
        self.db.set("b", "baz")
        self.db.begin()
        self.assertEqual(self.db.get("a"), "foo")
        self.db.set("a", "bar")
        self.assertEqual(self.db.count("bar"), 1)
        self.db.begin()
        self.assertEqual(self.db.count("bar"), 1)
        self.db.delete("a")
        self.assertEqual(self.db.get("a"), "NULL")
        self.assertEqual(self.db.count("bar"), 0)
        self.db.rollback()
        self.assertEqual(self.db.get("a"), "bar")
        self.assertEqual(self.db.count("bar"), 1)
        self.db.commit()
        self.assertEqual(self.db.get("a"), "bar")
        self.assertEqual(self.db.get("b"), "baz")


if __name__ == "__main__":
    unittest.main()
