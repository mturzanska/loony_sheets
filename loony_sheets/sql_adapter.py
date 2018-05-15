from collections import namedtuple


ParsedSqlStatement = namedtuple(
    'ParsedSqlStatement', (
        'columns',
        'sources',
        'conditions'
    )
)


class Column():

    @classmethod
    def from_string(cls, column_string):
        table_column = [s.strip() for s in column_string.split('.')]
        column = table_column.pop()
        table = table_column[0] if table_column else None
        return cls(table, column)

    def __init__(self, table, column):
        self.table = table
        self.column = column


class Condition():

    @classmethod
    def from_string(cls, condition_string):
        # TODO: add logic for 'is null' / 'is not null'
        elements = [s.strip() for s in condition_string.split()]
        if not elements:
            return None
        if len(elements) != 3:
            raise RuntimeError('Unknown condition format')
        return cls(*elements)

    def __init__(self, compared, sign=None, comparee=None):
        self.compared = compared
        self.sign = sign
        self.comparee = comparee


class Source():

    @classmethod
    def from_string(cls, source_string):
        table = source_string.strip()
        return cls(table)

    def __init__(self, table):
        self.table


Keywords = ('select', 'from', 'where')
InitialParserState = dict.fromkeys(Keywords, False)


class SqlPart():

    KEYWORD = None
    SEPARATOR = None
    PARSED_ENTITY = None

    def __init__(self):
        self.raw_elements = []
        self.parsed_elements = []

    def collect_elements(self, element):
        if element != self.KEYWORD:
            self.raw_elements.append(element)

    def parse(self):
        raw_sql = ' '.join(self.raw_elements)
        self.parsed_elements = [
            self.PARSED_ENTITY.from_string(element)
            for element in raw_sql.split(self.SEPARATOR)
        ]


class Select(SqlPart):

    SEPARATOR = ','


class From(SqlPart):

    KEYWORD = 'from'


class Where(SqlPart):

    KEYWORD = 'where'
    SEPARATOR = 'and'


class SqlStatement():

    def __init__(self, sql_string):
        self.sql_string = sql_string.lower()
        self.parsed_sql_statement = self._parse_sql()

    def _parse_sql(self):
        last_seen_keyword = 'select'
        sql_parts = [Select(), From(), Where()]
        sql_parts = {part.KEYWORD: part for part in sql_parts}

        elements = self.sql_string.split()
        for element in elements:
            sql_part = sql_parts.get(last_seen_keyword)
            sql_part.collect_elements(element)

        sql_parts = {
            keyword: part.parse()
            for keyword, part in sql_parts
        }

        return ParsedSqlStatement(
                    sql_parts.get('select'),
                    sql_parts.get('from'),
                    sql_parts.get('where'))
