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
from sqlalchemy.dialects.mysql.oursql \
    import MySQLDialect_oursql, _oursqlBIT
from sqlalchemy.sql import sqltypes

from .base import TiDBDialect


class TiDBDialect_oursql(MySQLDialect_oursql, TiDBDialect):
    colspecs = util.update_copy(
        TiDBDialect.colspecs, {sqltypes.Time: sqltypes.Time, BIT: _oursqlBIT}
    )


dialect = TiDBDialect_oursql
