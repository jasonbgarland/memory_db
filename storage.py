from enum import Enum
from typing import List


class TransactionType(str, Enum):
    """
    The list of possible commands that need to be rolled back in a transaction
    """
    SET = "SET"
    DELETE = "DELETE"


class Transaction:
    """
    A recorded transaction that might be rolled back later
    """
    def __init__(self, type: TransactionType, params: tuple, previous_value: str):
        self.type: TransactionType = type
        self.params = params
        self.previous_value = previous_value

    def __str__(self):
        return f"Transaction type: {self.type.value} | params: {self.params} | previous_value: {self.previous_value or None}"


class InMemoryDB:
    """
    In memory database using Python dicts (hash maps) for storage and retrieval.
    """
    def __init__(self):
        self.storage: dict = {}
        self.counts: dict = {}
        self.transactions: List[List[Transaction]] = []

    def get(self, name: str) -> str:
        """
        Gets a record for the given name.
        :param name: Name of the record to fetch from the DB
        :return: The value of the record. If the record does not exist "NULL" is returned
        """
        return self.storage.get(name, "NULL")

    def set(self, name: str, value: str, rollback=False):
        """
        Sets the value in the DB for the given record to the value provided.
        :param name: Name of the record to store. If the record exists, it will be updated.
        :param value: Value to store for the record.
        :param rollback: whether or not this transaction is a rollback transaction
        :return: None
        """
        prev_value = self.storage.get(name)

        # Don't do anything if the value hasn't changed
        if prev_value == value:
            return

        if rollback and value is None:
            # If we are rolling back an initial set of {name}, it's functionally a DELETE operation
            self.delete(name, rollback=True)
            return

        # Update value
        self.storage[name] = value
        # Update count of value
        # If this is a new value, the count defaults to 0, and we record that it is now a count of 1
        self.counts[value] = self.counts.get(value, 0) + 1

        # update count of previous value if we have changed a value
        if prev_value:
            self.counts[prev_value] = self.counts[prev_value] - 1

        if rollback is False and len(self.transactions) > 0:
            # if this isn't a rollback transaction, we record the action if we are in a transaction currently
            self.transactions[-1].append(
                Transaction(type=TransactionType.SET, params=(name, value), previous_value=prev_value))

    def delete(self, name: str, rollback=False):
        """
        Delete the record indicated by name.
        :param name: The name of the record to delete. If the record does not exist, no action will be performed.
        :param rollback: whether or not this transaction is a rollback transaction
        :return: None
        """
        # Delete the record.
        value = self.storage.pop(name, None)
        # If a record was deleted (if pop returned something), update the count of it's value
        if value:
            # TODO: here we are assuming count is always correct and that it should be above 0
            # but we guard against the DB not having a count for the value by setting the default to 0
            # there is probably a better way to do this
            self.counts[value] = self.counts.get(value, 0) - 1

            # We don't need to keep zero counts around
            if self.counts[value] == 0:
                self.counts.pop(value)

            if rollback is False and len(self.transactions) > 0:
                # if this isn't a rollback transaction, we record the action if we are in a transaction currently
                self.transactions[-1].append(
                    Transaction(type=TransactionType.DELETE, params=(name, value), previous_value=value))

    def count(self, value: str) -> int:
        """
        Return the number of records in the database that share the given value.
        :param value: Value to search on. If no records have that value, 0 will be returned.
        :return: The integer count of the number of records who share the value.
        """
        return self.counts.get(value, 0)

    def begin(self):
        """
        Begins a new transaction
        :return: None
        """
        # This sets up a new List to store transactions in our transactions store
        self.transactions.append([])

    def rollback(self):
        """
        Rools back the most recent transaction. If there is no transaction, rollback prints "TRANSACTION NOT FOUND"
        :return: None
        """
        if len(self.transactions) == 0:
            print("TRANSACTION NOT FOUND")
        else:
            # Go through all the transactions in the most recent transaction
            transactions_to_undo = self.transactions[-1]

            # Undo each transaction, starting from most recent
            for transaction in transactions_to_undo[::-1]:
                if transaction.type == "SET":
                    # reverse a SET, set the value to the previous value
                    name, _ = transaction.params
                    self.set(name, transaction.previous_value, rollback=True)
                if transaction.type == "DELETE":
                    # reverse a DELETE, which means set the value to what it was before delete
                    name, value = transaction.params
                    self.set(name, value, rollback=True)
            # lastly we remove the transactions from our list of transactions
            self.transactions.pop()

    def commit(self):
        """
        Commits ALL of the open transactions
        :return: None
        """
        # This finalizes all the data currenetly in the system,
        # meaning there are no transactions being stored to rollback
        self.transactions = []

    def __str__(self):
        """
        Override the str representation for the DB object so we can print out the DB for debugging
        :return: list of records in the DB along with their count
        """
        output = ["NAME       | VALUE      | COUNT"]
        for k in self.storage.keys():
            output.append(f"{k:10}   {self.storage[k]:10}   {self.counts.get(k, 0)}")
        return "\n".join(output)
