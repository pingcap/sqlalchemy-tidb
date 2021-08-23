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
from sqlalchemy import util, sql
from sqlalchemy.dialects.mysql.base import MySQLDialect, MySQLCompiler, \
    MySQLDDLCompiler, MySQLTypeCompiler, MySQLIdentifierPreparer, BIT
from sqlalchemy.engine import default, reflection

from . import reflection as _reflection

BIT = BIT


class TiDBCompiler(MySQLCompiler):
    pass


class TiDBDDLCompiler(MySQLDDLCompiler):
    pass


class TiDBTypeCompiler(MySQLTypeCompiler):
    pass


class TiDBIdentifierPreparer(MySQLIdentifierPreparer):
    pass


class TiDBDialect(MySQLDialect):
    name = "tidb"
    _needs_correct_for_88718_96365 = False
    supports_sequences = True
    supports_for_update_of = True
    tidb_version = (0, 0, 0)
    statement_compiler = TiDBCompiler
    ddl_compiler = TiDBDDLCompiler
    type_compiler = TiDBTypeCompiler
    preparer = TiDBIdentifierPreparer

    @property
    def _support_float_cast(self):
        if not self.server_version_info:
            return False
        return True

    @util.memoized_property
    def _tabledef_parser(self):
        """return the MySQLTableDefinitionParser, generate if needed.
        The deferred creation ensures that the dialect has
        retrieved server version information first.
        """
        preparer = self.identifier_preparer
        return _reflection.MySQLTableDefinitionParser(self, preparer)

    def initialize(self, connection):
        self._connection_charset = self._detect_charset(connection)
        self._detect_sql_mode(connection)
        self._detect_ansiquotes(connection)
        self._detect_casing(connection)
        if self._server_ansiquotes:
            # if ansiquotes == True, build a new IdentifierPreparer
            # with the new setting
            self.identifier_preparer = self.preparer(
                self, server_ansiquotes=self._server_ansiquotes
            )
        self.tidb_version = self._get_server_version_info(connection)

        default.DefaultDialect.initialize(self, connection)

    def has_sequence(self, connection, sequence_name, schema=None):
        if not self.supports_sequences:
            self._sequences_not_supported()
        if not schema:
            schema = self.default_schema_name
        # MariaDB implements sequences as a special type of table
        #
        cursor = connection.execute(
            sql.text(
                "SELECT SEQUENCE_NAME FROM INFORMATION_SCHEMA.SEQUENCES "
                "WHERE SEQUENCE_NAME=:name AND SEQUENCE_SCHEMA=:schema_name"
            ),
            dict(name=sequence_name, schema_name=schema),
        )
        return cursor.first() is not None

    @reflection.cache
    def get_sequence_names(self, connection, schema=None, **kw):
        if not self.supports_sequences:
            self._sequences_not_supported()
        if not schema:
            schema = self.default_schema_name
        # MariaDB implements sequences as a special type of table
        cursor = connection.execute(
            sql.text(
                "SELECT SEQUENCE_NAME FROM INFORMATION_SCHEMA.SEQUENCES "
                "WHERE SEQUENCE_SCHEMA=:schema_name"
            ),
            dict(schema_name=schema),
        )
        return [
            row[0]
            for row in self._compat_fetchall(
                cursor, charset=self._connection_charset
            )
        ]

    def _get_server_version_info(self, connection):
        # get database server version info explicitly over the wire
        # to avoid proxy servers like MaxScale getting in the
        # way with their own values, see #4205
        dbapi_con = connection.connection
        cursor = dbapi_con.cursor()
        cursor.execute("SELECT VERSION()")
        val = cursor.fetchone()[0]
        cursor.close()
        if util.py3k and isinstance(val, bytes):
            val = val.decode()

        return self._parse_server_version(val)

    def _parse_server_version(self, val):
        version_list = val.split('-')
        tidb_version_list = version_list[2].lstrip('v').split('.')
        if tidb_version_list != 'None':
            server_version_info = tuple(int(x) for x in tidb_version_list)
        else:
            server_version_info = (5,)

        self.server_version_info = server_version_info
        return server_version_info
