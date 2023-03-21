from typing import Optional, Union

from storage import InMemoryDB

help_text = \
    """
In memory DB. Available commands:

SET [name] [value]
    Sets the name in the database to the given value

GET [name]
    Prints the value for the given name. If the value is not in the database, prints NULL

DELETE [name]
    Deletes the value from the database

COUNT [value]
    Returns the number of names that have the given value assigned to them. If that value is not
    assigned anywhere, prints 0

END
    Exits the database

BEGIN
    Begins a new transaction

ROLLBACK
    Rolls back the most recent transaction. If there is no transaction to rollback, prints TRANSACTION
    NOT FOUND

COMMIT
    Commits all of the open transactions
"""


def process_commands(command: str, db: InMemoryDB) -> Optional[Union[str, int]]:
    """
    Parse a line of input from the user into a command for the DB, and run the command against the given DB
    :param command: Full line of input from the user
    :param db: InMemoryDB object to manipulate via the command
    :return: The return type and information will change depending upon the command
    """
    parsed = command.split()

    # Empty input is ignored
    if len(parsed) == 0:
        return

    cmd = parsed[0]

    if cmd == "SET":
        if len(parsed) == 3:
            name, value = parsed[1], parsed[2]
            db.set(name, value)
        else:
            print("SET requires two arguments: name and value")
    elif cmd == "GET":
        if len(parsed) == 2:
            name = parsed[1]
            print(db.get(name))
        else:
            print("GET requires one argument: name")
    elif cmd == "DELETE":
        if len(parsed) == 2:
            name = parsed[1]
            db.delete(name)
        else:
            print("DELETE requires one argument: name")
    elif cmd == "COUNT":
        if len(parsed) == 2:
            value = parsed[1]
            print(db.count(value))
        else:
            print("COUNT requires one argument: value")
    elif cmd == "END":
        if len(parsed) == 1:
            pass
        else:
            print("To exit the DB, use END command with no other arguments")
    elif cmd == "BEGIN":
        if len(parsed) == 1:
            db.begin()
        else:
            print("To BEGIN a transaction, use BEGIN command with no other arguments")
    elif cmd == "ROLLBACK":
        if len(parsed) == 1:
            db.rollback()
        else:
            print("To ROLLBACK a transaction, use ROLLBACK command with no other arguments")
    elif cmd == "COMMIT":
        if len(parsed) == 1:
            db.commit()
        else:
            print("To COMMIT a transaction, use COMMIT command with no other arguments")
    elif cmd == "SHOW":
        if len(parsed) == 1:
            print(db)
        else:
            print("To SHOW the state of the DB, use SHOW command with no other arguments")
    else:
        print(
            "Unrecognized command. Commands are case sensitive and should one of "
            "SET GET DELETE COUNT END BEGIN ROLLBACK or COMMIT")


if __name__ == "__main__":
    db = InMemoryDB()

    stop = False
    print(help_text)
    while stop is False:
        command = input(">> ")
        process_commands(command, db)

        if command.strip() == "END":
            stop = True
