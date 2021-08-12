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
from alembic.testing.requirements \
    import SuiteRequirements as SuiteRequirementsAlembic
from sqlalchemy.testing import exclusions, skip_if, fails_if, only_on, only_if
from sqlalchemy.testing.requirements \
    import SuiteRequirements as SuiteRequirementsSQLA


class Requirements(SuiteRequirementsSQLA, SuiteRequirementsAlembic):
    temporary_tables = exclusions.closed()
    temp_table_reflection = exclusions.closed()
    order_by_col_from_union = exclusions.open()
    time_microseconds = exclusions.closed()
    foreign_keys = exclusions.closed()

    @property
    def reflects_json_type(self):
        return only_on(["tidb"])

    @property
    def tidb_non_strict(self):
        def check(config):
            row = (
                config.db.connect(close_with_result=True)
                .exec_driver_sql("show variables like 'sql_mode'")
                .first()
            )
            return not row or "STRICT_TRANS_TABLES" not in row[1]

        return only_if(check)

    @property
    def tidb_zero_date(self):
        def check(config):
            row = (
                config.db.connect(close_with_result=True)
                .exec_driver_sql("show variables like 'sql_mode'")
                .first()
            )
            return not row or "NO_ZERO_DATE" not in row[1]

        return only_if(check)

    @property
    def datetime_microseconds(self):
        """target dialect supports representation of Python
        datetime.datetime() with microsecond objects."""

        return skip_if(
            ["tidb"]
        )

    @property
    def unicode_ddl(self):
        """Target driver must support some degree of non-ascii symbol names."""

        return only_on(["tidb"])

    @property
    def unbounded_varchar(self):
        """Target database must support VARCHAR with no length"""

        return skip_if(
            ["firebird", "oracle", "mysql", "mariadb", "tidb"],
            "not supported by database",
        )

    @property
    def independent_cursors(self):
        """Target must support simultaneous, independent database cursors
        on a single connection."""

        return skip_if(["tidb"], "no driver support")

    @property
    def self_referential_foreign_keys(self):
        """Target database must support self-referential foreign keys."""

        return exclusions.closed()

    @property
    def foreign_key_constraint_reflection(self):
        return exclusions.closed()

    @property
    def implicitly_named_constraints(self):
        return exclusions.open()

    @property
    def precision_generic_float_type(self):
        """target backend will return native floating point numbers with at
        least seven decimal places when using the generic Float type."""

        return fails_if(
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
                fails_if(
                    ["tidb"],
                    "Target backend can't accommodate full expressions in "
                    "OFFSET or LIMIT",
                )
                + self.offset
        )

    @property
    def table_ddl_if_exists(self):
        """target platform supports IF NOT EXISTS / IF EXISTS for tables."""
        return only_on(["tidb"])

    @property
    def index_ddl_if_exists(self):
        """target platform supports IF NOT EXISTS / IF EXISTS for indexes."""
        return only_on(["tidb"])

    @property
    def comment_reflection(self):
        return only_on(["tidb"])

    @property
    def mod_operator_as_percent_sign(self):
        """target database must use a plain percent '%' as the 'modulus'
        operator."""
        return only_if(["tidb"])
