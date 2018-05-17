import pytest

from loony_sheets.sql_adapter import Column
from loony_sheets.sql_adapter import Condition
from loony_sheets.sql_adapter import Source
from loony_sheets.sql_adapter import SqlStatement


column = 'a_column'
table = 'a_table'
condition = ('a_column', '>', '10')

raw_sql_1 = """
    SELECT {}
    FROM a_schema.{}
    WHERE {} {} {}
""".format(column, table, *condition)

parsed_sql_1 = SqlStatement(raw_sql_1)
parsed_sql_1.columns = [Column(column)]
parsed_sql_1.sources = [Source(table)]
parsed_sql_1.conditions = [Condition(*condition)]


@pytest.mark.parametrize('raw_sql,parsed_sql', [
    (raw_sql_1, parsed_sql_1),
])
def test_parse_sql(raw_sql, parsed_sql):

    sql_statement = SqlStatement(raw_sql)
    sql_statement.parse_sql()
    assert sql_statement == parsed_sql
