from loony_sheets.sql_adapter import Column
from loony_sheets.sql_adapter import Condition
from loony_sheets.sql_adapter import Source
from loony_sheets.sql_adapter import SqlStatement


def test_parse_sql():
    column = 'a_column'
    table = 'a_table'
    condition = ('a_column', '>', '10')

    sql_string = """
        SELECT {}
        FROM a_schema.{}
        WHERE {} {} {}
    """.format(column, table, *condition)

    expected_column = Column(column)
    expected_source = Source(table)
    expected_condition = Condition(*condition)
    expected_columns_count = 1
    expected_sources_count = 1
    expected_conditions_count = 1

    sql_statement = SqlStatement(sql_string)
    assert len(sql_statement.columns) == expected_columns_count
    assert len(sql_statement.sources) == expected_sources_count
    assert len(sql_statement.conditions) == expected_conditions_count
    assert sql_statement.columns[0] == expected_column
    assert sql_statement.sources[0] == expected_source
    assert sql_statement.conditions[0] == expected_condition
