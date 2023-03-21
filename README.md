# In Memory Databse

This project implements an in memory database that takes user commands one line at a time. 
It supports the following functions:

| Command   | Description                                                                                                                  |
|-----------|------------------------------------------------------------------------------------------------------------------------------|
| SET {name} {value} | Sets the name in the database to the given value                                                                             |
| GET {name} | Prints the value for the given name. If the value is not in the database, prints NULL                                        |
| DELETE {name} | Deletes the value from the database                                                                                          |
| COUNT {value} | Returns the number of names that have the given value assigned to them. If that value is not assigned anywhere, prints 0 |
| END | Exits the database |


In addition, the following transactional commands are supported:

| Command   | Description                                                                                                                  |
|-----------|------------------------------------------------------------------------------------------------------------------------------|
| BEGIN | Begins a new transaction |
| ROLLBACK | Rolls back the most recent transaction. If there is no transaction to rollback, prints TRANSACTION NOT FOUND |
| COMMIT | Commits all of the open transactions |

# Usage

## How to install

This was made in Python 3.10, with only standard libraries.  
It should work on most later versions of Python 3 but has not been extensively tested.   
No requirements will need to be installed other than a standard Python installation.

## How to run

Clone this repo and navigate to the root directory.

To run the in memory db use the following command:
```commandline
python memory_db.py
```

To run the unit tests associated with this project, use the following command:
```commandline
python test_memory_db.py
```

# Development notes:

## Environment

This was programmed in Python, since that is what I've been mainly developing in for the last 10 years or so.

## Data structures

### Records

The first thing to decide was how to organize and store the data in memory. There are included performance requirements:
  * Aim for GET, SET, DELETE, and COUNT to all have a runtime of less than O(log n), if not better
    (where n is the number of items in the database).

Looking at a quick reference chart:
https://www.bigocheatsheet.com/

My first thought was to use a tree structure to store the data. This would ensure that GET, SET, and DELETE
would all be done in O(log(n)) performance. However then we get to the COUNT command. Technically a red black tree can
have duplicate nodes, but most implementations don't take that into account, and I don't want to get bogged down
using up the whole time estimate on debugging a red black tree when there are a lot of requirements to fulfill.

This lead me to looking at a hash table as a solution, which actually would be faster for the average use cases - being O(1).
The downside here is that the worst case scenarios would be O(n) which is outside our performance requirements.

A natural solution in Python is to use dicts, which are implemented via hash maps.  The Python wiki confirms that dicts use hash maps:
https://wiki.python.org/moin/TimeComplexity

And then after worrying about the worst case being O(n) for operations, I found that this is only the absolute worst
case when the hash function resolves every incoming value to the same key, which is probably not going to be the case for
us.  If there is time eventually, we can do performance testing and override __hash__ with a better hash function or swap
out the underlying storage as necessary.

### COUNT

A separate Python dict is used to keep track of the counts of each value in the system, for faster lookup. Counts are 
updated on SET and DELETE operations.

### TRANSACTIONS

A list data structure (array in Python) is used to store groups of transactions that are in use. Each group of transactions
is a list of Transaction objects, which contain the type of transaction, call details, and previous value in the system
before the statement was executed.

We add transaction groups to the list in the order they are created. To rollback a transaction, we grab the transaction
group at the end of the list, and reverse each transaction in the group in reverse order. Once that is done the 
transaction can be removed from the list.

