# sqlalchemy-tidb

[![.github/workflows/ci.yml](https://github.com/pingcap/sqlalchemy-tidb/actions/workflows/ci.yml/badge.svg)](https://github.com/pingcap/sqlalchemy-tidb/actions/workflows/ci.yml)

This adds compatibility for [TiDB](https://github.com/pingcap/tidb) to SQLAlchemy.

## Supported versions

- TiDB 4.x and newer
- SQLAlchemy 1.4.x
- Python 3.6 and newer

## Installation

```shell
pip install git+https://github.com/pingcap/sqlalchemy-tidb.git@main
# install driver, the default driver is mysql-connector-python
pip install mysql-connector-python
```

## Getting Started

In your Python app, you can connect to the database via:

```python
from sqlalchemy import create_engine
engine = create_engine("tidb://username:password@ip:port/database_name?charset=utf8mb4")
```

## testing

You can run the tests using the following command:

```shell
tox
```

## Known issues

- TiDB does not support FOREIGN KEY constraints until v6.6.0([#18209](https://github.com/pingcap/tidb/issues/18209)).
- TiDB does not support SAVEPOINT until v6.2.0([#6840](https://github.com/pingcap/tidb/issues/6840)).

## Connect to TiDB Cloud Serverless

TiDB Serverless offers the TiDB database with full HTAP capabilities for you and your organization. It is a fully managed, auto-scaling deployment of TiDB that lets you start using your database immediately, develop and run your application without caring about the underlying nodes, and automatically scale based on your application's workload changes.

### 0. Signup to [TiDB Cloud](https://tidbcloud.com/signup?utm_source=github&utm_medium=sqlalchemy_tidb)

### 1. Create a [serverless cluster](https://tidbcloud.com/console/clusters/create-cluster?utm_source=github&utm_medium=sqlalchemy_tidb)

### 2. Obtain TiDB serverless [connection parameters](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection-serverless#obtain-tidb-serverless-connection-parameters)

Example

```text
host: 'gateway01.us-east-1.prod.aws.tidbcloud.com',
port: 4000,
user: 'xxxxxx.root',
password: '<your_password>',
ssl_ca: /etc/ssl/cert.pem   # macos
```

### 3. Determain your root certificate based on your system

[Root certificate default path](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters#root-certificate-default-path)

### 4. Connect to Serverless cluster

```python
from sqlalchemy import create_engine, text

engine = create_engine(
    "tidb://{user}:{password}@{host}:{port}/test?charset=utf8mb4",
    connect_args={'ssl_ca': '/etc/ssl/cert.pem', 'ssl_verify_identity': True}
)

with engine.connect() as con:
    result = con.execute(text("show databases;"))
    print(result.fetchall())
```
