# sqlalchemy-tidb

[![.github/workflows/ci.yml](https://github.com/pingcap/sqlalchemy-tidb/actions/workflows/ci.yml/badge.svg)](https://github.com/pingcap/sqlalchemy-tidb/actions/workflows/ci.yml)

This adds compatibility for [TiDB](https://github.com/pingcap/tidb) to SQLAlchemy.

## Supported versions

- TiDB 4.x and newer
- SQLAlchemy 1.4.x
- Python 3.6 and newer

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

## Known issues

- TiDB does not support FOREIGN KEY constraints until v6.6.0([#18209](https://github.com/pingcap/tidb/issues/18209)).
- TiDB does not support SAVEPOINT until v6.2.0([#6840](https://github.com/pingcap/tidb/issues/6840)).