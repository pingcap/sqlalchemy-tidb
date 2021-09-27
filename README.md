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