# sqlalchemy-tidb

[![.github/workflows/ci.yml](https://github.com/pingcap/sqlalchemy-tidb/actions/workflows/ci.yml/badge.svg)](https://github.com/pingcap/sqlalchemy-tidb/actions/workflows/ci.yml)

This adds compatibility for [TiDB](https://github.com/pingcap/tidb) to SQLAlchemy.

## Supported versions

- TiDB 4.x and newer
- SQLAlchemy 1.4.x
- Python 3.6 and newer

## Installation

```bash
pip install git+https://github.com/pingcap/sqlalchemy-tidb.git@main
```

## Getting Started

In your Python app, you can connect to the database via:

```python
from sqlalchemy import create_engine
engine = create_engine("tidb://username:password@ip:port/database_name?charset=utf8mb4")
```

## testing

You can run the tests using the following command:

```bash
tox
# or test for a specified python version
tox -e py39
```

## Known issues

- TiDB only support `TIFLASH REPLICA` since v4.0.0([#](https://github.com/pingcap/tidb/)).
- TiDB only support `FOREIGN KEY` constraints since v6.6.0([#18209](https://github.com/pingcap/tidb/issues/18209)).
- TiDB only support `SAVEPOINT` since v6.2.0([#6840](https://github.com/pingcap/tidb/issues/6840)).
- TiDB only support `VECTOR INDEX` since v8.4.0([#54245](https://github.com/pingcap/tidb/issues/54245)).
