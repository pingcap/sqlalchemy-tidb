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
from sqlalchemy.dialects.mysql.mysqldb \
    import MySQLDialect_mysqldb

from .base import TiDBCompiler
from .base import TiDBDDLCompiler
from .base import TiDBDialect
from .base import TiDBIdentifierPreparer


class TiDBDialect_mysqldb(MySQLDialect_mysqldb, TiDBDialect):
    name = "tidb"
    driver = "mysqldb"
    supports_statement_cache = True

    supports_unicode_binds = True

    supports_sane_rowcount = True
    supports_sane_multi_rowcount = True

    supports_native_decimal = True

    default_paramstyle = "format"
    ddl_compiler = TiDBDDLCompiler
    statement_compiler = TiDBCompiler

    preparer = TiDBIdentifierPreparer


dialect = TiDBDialect_mysqldb
