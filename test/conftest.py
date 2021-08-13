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

import pytest
from sqlalchemy.dialects import registry

registry.register(
    "tidb",
    "sqlalchemy_tidb.mysqldb",
    "TiDBDialect_mysqldb"
)

# sqlalchemy's dialect-testing machinery wants an entry like this.
# It is wack. :(
registry.register(
    "tidb.mysqldb",
    "sqlalchemy_tidb.mysqldb",
    "TiDBDialect_mysqldb",
)

pytest.register_assert_rewrite("sqlalchemy.testing.assertions")

from sqlalchemy.testing.plugin.pytestplugin import *  # noqa
