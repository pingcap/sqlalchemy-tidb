# Copyright 2021 PingCAP, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# See the License for the specific language governing permissions and
# limitations under the License.

from sqlalchemy import testing, inspect
from sqlalchemy.testing import eq_
from sqlalchemy.testing.suite import *  # noqa

from sqlalchemy.testing.suite import QuotedNameArgumentTest \
    as _QuotedNameArgumentTest
from sqlalchemy.testing.suite import ComponentReflectionTest \
    as _ComponentReflectionTest
from sqlalchemy.testing.suite import config


class QuotedNameArgumentTest(_QuotedNameArgumentTest):
    @_QuotedNameArgumentTest.quote_fixtures
    def test_get_foreign_keys(self, name):
        if config.db.dialect.tidb_version >= (6, 6, 0):
            super().test_get_foreign_keys(name, None)


class ComponentReflectionTest(_ComponentReflectionTest):
    @testing.combinations(
        (False,), (True, testing.requires.schemas), argnames="use_schema"
    )
    @testing.requires.foreign_key_constraint_reflection
    def test_get_foreign_keys(self, connection, use_schema):
        if use_schema:
            schema = config.test_schema
        else:
            schema = None

        users, addresses = (self.tables.users, self.tables.email_addresses)
        insp = inspect(connection)

        if testing.requires.self_referential_foreign_keys.enabled:
            users_fkeys = insp.get_foreign_keys(users.name, schema=schema)
            fkey1 = users_fkeys[0]

            with testing.requires.named_constraints.fail_if():
                eq_(fkey1["name"], "user_id_fk")

            eq_(fkey1["referred_table"], users.name)
            eq_(fkey1["referred_columns"], ["user_id"])
            if testing.requires.self_referential_foreign_keys.enabled:
                eq_(fkey1["constrained_columns"], ["parent_user_id"])

        # addresses
        addr_fkeys = insp.get_foreign_keys(addresses.name, schema=schema)
        fkey1 = addr_fkeys[0]

        with testing.requires.implicitly_named_constraints.fail_if():
            self.assert_(fkey1["name"] is not None)

        eq_(fkey1["referred_table"], users.name)
        eq_(fkey1["referred_columns"], ["user_id"])
        eq_(fkey1["constrained_columns"], ["remote_user_id"])
