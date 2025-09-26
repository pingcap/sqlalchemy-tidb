# sqlalchemy-tidb

> [!IMPORTANT]
>
> This repository was archived and is no longer maintained (no new issues or PRs)
>
>
> Please use [SQLAlchemy](https://www.sqlalchemy.org/) with the MySQL dialect to connect to TiDB — no extra third-party dialect is required.
> For setup instructions and examples, see the official TiDB guide: https://docs.pingcap.com/tidb/stable/dev-guide-sample-application-python-sqlalchemy/

[![.github/workflows/ci.yml](https://github.com/pingcap/sqlalchemy-tidb/actions/workflows/ci.yml/badge.svg)](https://github.com/pingcap/sqlalchemy-tidb/actions/workflows/ci.yml)

This adds compatibility for [TiDB](https://github.com/pingcap/tidb) to SQLAlchemy.

## Supported versions

- TiDB 4.x and newer
- SQLAlchemy 1.4.x
- Python 3.8 and newer

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

## Known issues

- TiDB only support `FOREIGN KEY` constraints since v6.6.0([#18209](https://github.com/pingcap/tidb/issues/18209)).
- TiDB only support `SAVEPOINT` since v6.2.0([#6840](https://github.com/pingcap/tidb/issues/6840)).

## Testing this dialect with SQLAlchemy and Alembic

Bootstrap your environment with virtualenv and requirements installed

```bash
make bootstrap
```

You can run the tests using the following command:

```bash
make all
# Or running test with `tox` for a specified python version
tox -e py39
# Or running test directly using `pytest`
pytest "test/test_suite.py::DateTest"
```

To know more about developing the TiDB dialect, checkout the guide on sqlalchemy:

* https://github.com/sqlalchemy/sqlalchemy/blob/rel_1_4/README.dialects.rst
* https://github.com/sqlalchemy/sqlalchemy/blob/rel_1_4/README.unittests.rst
