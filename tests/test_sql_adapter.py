from loony_sheets.sql_adapter import SqlStatement


def test_parse_sql(simple_sql):
    raw_sql, parsed_sql = simple_sql
    sql_statement = SqlStatement(raw_sql)
    sql_statement.parse_sql()
    assert sql_statement.sources == parsed_sql.sources
    assert sql_statement.columns == parsed_sql.columns
    assert sql_statement.conditions == parsed_sql.conditions
