# sqlalchemy-tidb

This adds compatibility for [TiDB](https://github.com/pingcap/tidb) to Django.


## Supported versions

- TiDB 5.x (tested with 5.1.x)
- SQLAlchemy 1.4.x
- Python 3.6 an newer (tested with Python 3.9)

## Installation

```
pip install git+https://github.com/pingcap/sqlalchemy-tidb.git@main
```

## Getting Started

In your Python app, you can connect to the database via:

```
from sqlalchemy import create_engine
engine = create_engine("tidb://username:password@ip:port/database_name?charset=utf8mb4")
```

## testing

You can run the tests using the following command:

```
tox
```