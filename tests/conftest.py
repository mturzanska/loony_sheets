from pathlib import Path

import pytest

from loony_sheets import config
from loony_sheets.sql_adapter import Column
from loony_sheets.sql_adapter import Condition
from loony_sheets.sql_adapter import Source
from loony_sheets.sql_adapter import SqlStatement


@pytest.fixture
def test_env(mocker):
    root_dir = Path('.').parent
    TEST_SECRET = Path(root_dir, 'client_secret.json')
    mocker.patch.object(config, 'SECRET', TEST_SECRET)


def get_raw_select(columns):
    if isinstance(columns, dict):
        columns = ', '.join([
            ' as '.join(k, v) for k, v in columns.items()
        ])
    else:
        columns = ', '.join(columns)
    return 'select ' + columns


def get_raw_from(tables):
    if isinstance(tables, list):
        if len(tables) == 1:
            return 'from ' + tables[0]
        else:
            pass

    if isinstance(tables, dict):
        pass


def get_raw_where(conditions):
    if isinstance(conditions, list):
        conditions = ' and '.join(conditions)
    return 'where ' + conditions


def get_raw_sql(columns, tables, conditions):
    raw_select = get_raw_select(columns)
    raw_from = get_raw_from(tables)
    raw_where = get_raw_where(conditions)
    return ' '.join([raw_select, raw_from, raw_where])


def get_parsed_sql(columns, tables, conditions):
    parsed_sql = SqlStatement()
    parsed_sql.columns = [Column.from_string(c) for c in columns]
    parsed_sql.sources = [Source.from_string(t) for t in tables]
    parsed_sql.conditions = [Condition.from_string(c) for c in conditions]
    return parsed_sql


def get_raw_and_parsed_sql(columns, tables, conditions):
    raw_sql = get_raw_sql(columns, tables, conditions)
    parsed_sql = get_parsed_sql(columns, tables, conditions)
    return (raw_sql, parsed_sql)


@pytest.fixture
def simple_sql():
    columns = ['a_column']
    tables = ['a_table']
    conditions = ['a_column > 10']
    return get_raw_and_parsed_sql(columns, tables, conditions)
