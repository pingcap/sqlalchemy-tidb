# Copyright 2021 PingCAP, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# See the License for the specific language governing permissions and
# limitations under the License.
from sqlalchemy import exc
from sqlalchemy.testing.provision import configure_follower
from sqlalchemy.testing.provision import create_db
from sqlalchemy.testing.provision import drop_db
from sqlalchemy.testing.provision import generate_driver_url
from sqlalchemy.testing.provision import temp_table_keyword_args


@generate_driver_url.for_db("tidb")
def generate_driver_url(url, driver, query_str):
    backend = url.get_backend_name()

    # NOTE: at the moment, tests are running mariadbconnector
    # against both mariadb and mysql backends.   if we want this to be
    # limited, do the decision making here to reject a "mysql+mariadbconnector"
    # URL.  Optionally also re-enable the module level
    # MySQLDialect_mariadbconnector.is_mysql flag as well, which must include
    # a unit and/or functional test.

    # all the Jenkins tests have been running mysqlclient Python library
    # built against mariadb client drivers for years against all MySQL /
    # MariaDB versions going back to MySQL 5.6, currently they can talk
    # to MySQL databases without problems.
    new_url = url.set(
        drivername="%s+%s" % (backend, driver)
    ).update_query_string(query_str)

    try:
        new_url.get_dialect()
    except exc.NoSuchModuleError:
        return None
    else:
        return new_url


@create_db.for_db("tidb")
def _tidb_create_db(cfg, eng, ident):
    with eng.begin() as conn:
        try:
            _tidb_drop_db(cfg, conn, ident)
        except Exception:
            pass

    with eng.begin() as conn:
        conn.exec_driver_sql(
            "CREATE DATABASE %s CHARACTER SET utf8mb4" % ident
        )
        conn.exec_driver_sql(
            "CREATE DATABASE %s_test_schema CHARACTER SET utf8mb4" % ident
        )
        conn.exec_driver_sql(
            "CREATE DATABASE %s_test_schema_2 CHARACTER SET utf8mb4" % ident
        )


@configure_follower.for_db("tidb")
def _tidb_configure_follower(config, ident):
    config.test_schema = "%s_test_schema" % ident
    config.test_schema_2 = "%s_test_schema_2" % ident


@drop_db.for_db("tidb")
def _tidb_drop_db(cfg, eng, ident):
    with eng.begin() as conn:
        conn.exec_driver_sql("DROP DATABASE %s_test_schema" % ident)
        conn.exec_driver_sql("DROP DATABASE %s_test_schema_2" % ident)
        conn.exec_driver_sql("DROP DATABASE %s" % ident)


@temp_table_keyword_args.for_db("tidb")
def _mysql_temp_table_keyword_args(cfg, eng):
    return {"prefixes": ["TEMPORARY"]}
