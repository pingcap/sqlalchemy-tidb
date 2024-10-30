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
from sqlalchemy.testing import exclusions
from alembic.testing.requirements \
    import SuiteRequirements as SuiteRequirementsAlembic
from sqlalchemy.testing.requirements \
    import SuiteRequirements as SuiteRequirementsSQLA


class Requirements(SuiteRequirementsSQLA, SuiteRequirementsAlembic):
    order_by_col_from_union = exclusions.open()
    time_microseconds = exclusions.closed()
    datetime_microseconds = exclusions.closed()
    autocommit = exclusions.open()
    views = exclusions.open()
    regexp_match = exclusions.open()
    sequences_optional = exclusions.open()
    unicode_ddl = exclusions.open()
    unbounded_varchar = exclusions.closed()
    independent_cursors = exclusions.closed()
    implicitly_named_constraints = exclusions.open()
    table_ddl_if_exists = exclusions.open()
    index_ddl_if_exists = exclusions.open()
    comment_reflection = exclusions.open()
    mod_operator_as_percent_sign = exclusions.open()
    # https://github.com/pingcap/tidb/issues/45181
    ctes = exclusions.closed()

    regexp_replace = exclusions.skip_if(
        lambda config: config.db.dialect.tidb_version < (6, 5, 0),
        'versions before 6.5.0 do not support regexp_replace',
    )

    isolation_level = exclusions.open()
    legacy_isolation_level = exclusions.open()

    def get_isolation_levels(self, config):
        return {
            "default": "REPEATABLE READ",
            "supported": [
                "READ COMMITTED", "REPEATABLE READ",
                "AUTOCOMMIT"
            ]
        }

    def get_order_by_collation(self, config):
        return 'utf8mb4_bin'

    ad_hoc_engines = exclusions.open()

    temporary_tables = exclusions.skip_if(
        lambda config: config.db.dialect.tidb_version < (5, 3, 0),
        'versions before 5.3.0 do not support temporary tables',
    )
    # TiDB doesn't support CREATE INDEX for local temporary table
    temp_table_reflect_indexes = exclusions.closed()
    temp_table_reflection = exclusions.closed()

    # https://github.com/pingcap/tidb/issues/45071
    json_type = exclusions.closed()
    reflects_json_type = exclusions.closed()

    foreign_keys = exclusions.skip_if(
        lambda config: config.db.dialect.tidb_version < (6, 6, 0),
        'versions before 6.6.0 do not support foreign key reflection',
    )
    foreign_key_constraint_reflection = foreign_keys
    self_referential_foreign_keys = foreign_keys

    savepoints = exclusions.skip_if(
        lambda config: config.db.dialect.tidb_version < (6, 2, 0),
        'versions before 6.2.0 do not support savepoints',
    )
    savepoints_w_release = savepoints
    compat_savepoints = savepoints

    updateable_autoincrement_pks = exclusions.open()

    @property
    def tidb_non_strict(self):
        def check(config):
            row = (
                config.db.connect(close_with_result=True)
                .exec_driver_sql("show variables like 'sql_mode'")
                .first()
            )
            return not row or "STRICT_TRANS_TABLES" not in row[1]

        return exclusions.only_if(check)

    @property
    def tidb_zero_date(self):
        def check(config):
            row = (
                config.db.connect(close_with_result=True)
                .exec_driver_sql("show variables like 'sql_mode'")
                .first()
            )
            return not row or "NO_ZERO_DATE" not in row[1]

        return exclusions.only_if(check)

    @property
    def precision_generic_float_type(self):
        """target backend will return native floating point numbers with at
        least seven decimal places when using the generic Float type."""

        return exclusions.fails_if(
            [
                (
                    "tidb",
                    None,
                    None,
                    "tidb FLOAT type only returns 4 decimals",
                ),
            ]
        )

    @property
    def sql_expression_limit_offset(self):
        return (
                exclusions.fails_if(
                    ["tidb"],
                    "Target backend can't accommodate full expressions in "
                    "OFFSET or LIMIT",
                )
                + self.offset
        )

    @property
    def datetime_implicit_bound(self):
        return exclusions.fails_on(
            ["mysql", "mariadb", "tidb"]
        )
