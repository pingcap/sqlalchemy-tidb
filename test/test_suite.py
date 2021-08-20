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

from sqlalchemy.testing.suite import *  # noqa

from sqlalchemy.testing.suite import QuotedNameArgumentTest \
    as _QuotedNameArgumentTest
from sqlalchemy.testing.suite import config


class QuotedNameArgumentTest(_QuotedNameArgumentTest):
    @_QuotedNameArgumentTest.quote_fixtures
    def test_get_foreign_keys(self, name):
        if config.db.dialect.tidb_version >= (5,):
            super().test_get_foreign_keys(name, None)
