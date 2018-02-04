from collections import namedtuple
import string


ParsedSqlStatement = namedtuple(
    'ParsedSqlStatement', (
        'columns',
        'sources',
        'conditions'
    )
)


class SqlStatement(object):

    def __init__(self, sql_string):
        self.sql_string = sql_string.lower()
        self.parsed_sql_statement = self._parse_sql()

    def _parse_sql(self):
        columns = []
        sources = []
        conditions = []
        in_columns = in_sources = in_conditions = False

        tokens = self.sql_string.split()
        for token in tokens:

            if token == 'select':
                in_columns = True
                in_sources = False
                in_conditions = False
                continue

            if token == 'from':
                in_columns = False
                in_sources = True
                in_conditions = False
                continue

            if token == 'where':
                in_columns = False
                in_sources = False
                in_conditions = True
                continue

            if in_columns:
                if token in string.punctuation:
                    continue
                columns.append(token)
            if in_sources:
                if token in string.punctuation:
                    continue
                sources.append(token)
            if in_conditions:
                conditions.append(token)

        return ParsedSqlStatement(columns, sources, conditions)
