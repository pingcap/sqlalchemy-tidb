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
from sqlalchemy import util
from sqlalchemy.dialects.mysql.base import BIT
from sqlalchemy.dialects.mysql.cymysql \
    import MySQLDialect_cymysql, _cymysqlBIT

from .base import TiDBDialect


class TiDBDialect_cymysql(MySQLDialect_cymysql):
    driver = "cymysql"

    colspecs = util.update_copy(TiDBDialect.colspecs, {BIT: _cymysqlBIT})


dialect = TiDBDialect_cymysql
