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
import re

from sqlalchemy import log
from sqlalchemy.dialects.mysql.reflection import MySQLTableDefinitionParser, \
    _pr_compile, _re_compile, _options_of_type_string


@log.class_logger
class TidbTableDefinitionParser(MySQLTableDefinitionParser):
    # https://github.com/sqlalchemy/sqlalchemy/pull/6660
    def _prep_regexes(self):
        """Pre-compile regular expressions."""

        self._re_columns = []
        self._pr_options = []

        _final = self.preparer.final_quote

        quotes = dict(
            zip(
                ("iq", "fq", "esc_fq"),
                [
                    re.escape(s)
                    for s in (
                        self.preparer.initial_quote,
                        _final,
                        self.preparer._escape_identifier(_final),
                    )
                ],
            )
        )

        self._pr_name = _pr_compile(
            r"^CREATE (?:\w+ +)?TABLE +"
            r"%(iq)s(?P<name>(?:%(esc_fq)s|[^%(fq)s])+)%(fq)s +\($" % quotes,
            self.preparer._unescape_identifier,
        )

        # `col`,`col2`(32),`col3`(15) DESC
        #
        self._re_keyexprs = _re_compile(
            r"(?:"
            r"(?:%(iq)s((?:%(esc_fq)s|[^%(fq)s])+)%(fq)s)"
            r"(?:\((\d+)\))?(?: +(ASC|DESC))?(?=\,|$))+" % quotes
        )

        # 'foo' or 'foo','bar' or 'fo,o','ba''a''r'
        self._re_csv_str = _re_compile(r"\x27(?:\x27\x27|[^\x27])*\x27")

        # 123 or 123,456
        self._re_csv_int = _re_compile(r"\d+")

        # `colname` <type> [type opts]
        #  (NOT NULL | NULL)
        #   DEFAULT ('value' | CURRENT_TIMESTAMP...)
        #   COMMENT 'comment'
        #  COLUMN_FORMAT (FIXED|DYNAMIC|DEFAULT)
        #  STORAGE (DISK|MEMORY)
        self._re_column = _re_compile(
            r"  "
            r"%(iq)s(?P<name>(?:%(esc_fq)s|[^%(fq)s])+)%(fq)s +"
            r"(?P<coltype>\w+)"
            r"(?:\((?P<arg>(?:\d+|\d+,\d+|"
            r"(?:'(?:''|[^'])*',?)+))\))?"
            r"(?: +(?P<unsigned>UNSIGNED))?"
            r"(?: +(?P<zerofill>ZEROFILL))?"
            r"(?: +CHARACTER SET +(?P<charset>[\w_]+))?"
            r"(?: +COLLATE +(?P<collate>[\w_]+))?"
            r"(?: +(?P<notnull>(?:NOT )?NULL))?"
            r"(?: +DEFAULT +(?P<default>"
            r"(?:NULL|'(?:''|[^'])*'|[\-\w\.\(\)]+"
            r"(?: +ON UPDATE [\-\w\.\(\)]+)?)"
            r"))?"
            r"(?: +(?:GENERATED ALWAYS)? ?AS +(?P<generated>\("
            r".*\))? ?(?P<persistence>VIRTUAL|STORED)?)?"
            r"(?: +(?P<autoincr>AUTO_INCREMENT))?"
            r"(?: +COMMENT +'(?P<comment>(?:''|[^'])*)')?"
            r"(?: +COLUMN_FORMAT +(?P<colfmt>\w+))?"
            r"(?: +STORAGE +(?P<storage>\w+))?"
            r"(?: +(?P<extra>.*))?"
            r",?$" % quotes
        )

        # Fallback, try to parse as little as possible
        self._re_column_loose = _re_compile(
            r"  "
            r"%(iq)s(?P<name>(?:%(esc_fq)s|[^%(fq)s])+)%(fq)s +"
            r"(?P<coltype>\w+)"
            r"(?:\((?P<arg>(?:\d+|\d+,\d+|\x27(?:\x27\x27|[^\x27])+\x27))\))?"
            r".*?(?P<notnull>(?:NOT )NULL)?" % quotes
        )

        # (PRIMARY|UNIQUE|FULLTEXT|SPATIAL) INDEX `name` (USING (BTREE|HASH))?
        # (`col` (ASC|DESC)?, `col` (ASC|DESC)?)
        # KEY_BLOCK_SIZE size | WITH PARSER name  /*!50100 WITH PARSER name */
        self._re_key = _re_compile(
            r"  "
            r"(?:(?P<type>\S+) )?KEY"
            r"(?: +%(iq)s(?P<name>(?:%(esc_fq)s|[^%(fq)s])+)%(fq)s)?"
            r"(?: +USING +(?P<using_pre>\S+))?"
            r" +\((?P<columns>.+?)\)"
            r"(?: +USING +(?P<using_post>\S+))?"
            r"(?: +KEY_BLOCK_SIZE *[ =]? *(?P<keyblock>\S+))?"
            r"(?: +WITH PARSER +(?P<parser>\S+))?"
            r"(?: +COMMENT +(?P<comment>(\x27\x27|\x27([^\x27])*?\x27)+))?"
            r"(?: +/\*(?P<version_sql>.+)\*/ +)?"
            r",?$" % quotes
        )

        # https://forums.mysql.com/read.php?20,567102,567111#msg-567111
        # It means if the MySQL version >= \d+, execute what's in the comment
        self._re_key_version_sql = _re_compile(
            r"\!\d+ " r"(?: *WITH PARSER +(?P<parser>\S+) *)?"
        )

        # CONSTRAINT `name` FOREIGN KEY (`local_col`)
        # REFERENCES `remote` (`remote_col`)
        # MATCH FULL | MATCH PARTIAL | MATCH SIMPLE
        # ON DELETE CASCADE ON UPDATE RESTRICT
        #
        # unique constraints come back as KEYs
        kw = quotes.copy()
        kw["on"] = "RESTRICT|CASCADE|SET NULL|NO ACTION"
        self._re_fk_constraint = _re_compile(
            r"  "
            r"CONSTRAINT +"
            r"%(iq)s(?P<name>(?:%(esc_fq)s|[^%(fq)s])+)%(fq)s +"
            r"FOREIGN KEY +"
            r"\((?P<local>[^\)]+?)\) REFERENCES +"
            r"(?P<table>%(iq)s[^%(fq)s]+%(fq)s"
            r"(?:\.%(iq)s[^%(fq)s]+%(fq)s)?) +"
            r"\((?P<foreign>[^\)]+?)\)"
            r"(?: +(?P<match>MATCH \w+))?"
            r"(?: +ON DELETE (?P<ondelete>%(on)s))?"
            r"(?: +ON UPDATE (?P<onupdate>%(on)s))?" % kw
        )

        # CONSTRAINT `CONSTRAINT_1` CHECK (`x` > 5)'
        # testing on MariaDB 10.2 shows that the CHECK constraint
        # is returned on a line by itself, so to match without worrying
        # about parenthesis in the expression we go to the end of the line
        self._re_ck_constraint = _re_compile(
            r"  "
            r"CONSTRAINT +"
            r"%(iq)s(?P<name>(?:%(esc_fq)s|[^%(fq)s])+)%(fq)s +"
            r"CHECK +"
            r"\((?P<sqltext>.+)\),?" % kw
        )

        # PARTITION
        #
        # punt!
        self._re_partition = _re_compile(r"(?:.*)(?:SUB)?PARTITION(?:.*)")

        # Table-level options (COLLATE, ENGINE, etc.)
        # Do the string options first, since they have quoted
        # strings we need to get rid of.
        for option in _options_of_type_string:
            self._add_option_string(option)

        for option in (
                "ENGINE",
                "TYPE",
                "AUTO_INCREMENT",
                "AVG_ROW_LENGTH",
                "CHARACTER SET",
                "DEFAULT CHARSET",
                "CHECKSUM",
                "COLLATE",
                "DELAY_KEY_WRITE",
                "INSERT_METHOD",
                "MAX_ROWS",
                "MIN_ROWS",
                "PACK_KEYS",
                "ROW_FORMAT",
                "KEY_BLOCK_SIZE",
        ):
            self._add_option_word(option)

        self._add_option_regex("UNION", r"\([^\)]+\)")
        self._add_option_regex("TABLESPACE", r".*? STORAGE DISK")
        self._add_option_regex(
            "RAID_TYPE",
            r"\w+\s+RAID_CHUNKS\s*\=\s*\w+RAID_CHUNKSIZE\s*=\s*\w+",
        )
