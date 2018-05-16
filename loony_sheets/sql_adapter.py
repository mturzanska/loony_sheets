class ParsedSqlPart():

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return False


class Column(ParsedSqlPart):

    @classmethod
    def from_string(cls, column_string):
        table_column = [s.strip() for s in column_string.split('.')]
        column = table_column.pop()
        table = table_column[0] if table_column else None
        return cls(column, table)

    def __init__(self, name, table=None):
        self.table = table
        self.name = name


class Condition(ParsedSqlPart):

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


class Source(ParsedSqlPart):

    # TODO: add logic for handling aliases

    @classmethod
    def from_string(cls, source_string):
        schema_table = [s.strip() for s in source_string.split('.')]
        table = schema_table[-1]
        return cls(table)

    def __init__(self, table):
        self.table = table


class RawSqlPart():

    KEYWORD = None
    SEPARATOR = None
    PARSED_ENTITY = None

    def __init__(self):
        self.raw_elements = []

    def collect_elements(self, element):
        if element != self.KEYWORD:
            self.raw_elements.append(element)

    def parse(self):
        raw_sql = ' '.join(self.raw_elements)
        return [
            self.PARSED_ENTITY.from_string(element)
            for element in raw_sql.split(self.SEPARATOR)
        ]


class Select(RawSqlPart):

    KEYWORD = 'select'
    PARSED_ENTITY = Column
    SEPARATOR = ','


class From(RawSqlPart):

    KEYWORD = 'from'
    PARSED_ENTITY = Source


class Where(RawSqlPart):

    KEYWORD = 'where'
    PARSED_ENTITY = Condition
    SEPARATOR = 'and'


class SqlStatement():

    def __init__(self, sql_string):
        self.sql_string = sql_string.lower()
        self.columns, self.sources, self.conditions = self._parse_sql()

    def _parse_sql(self):
        last_seen_keyword = 'select'
        sql_parts = [Select(), From(), Where()]
        sql_parts = {part.KEYWORD: part for part in sql_parts}

        elements = self.sql_string.split()
        for element in elements:
            if element in sql_parts:
                last_seen_keyword = element
            sql_part = sql_parts.get(last_seen_keyword)
            sql_part.collect_elements(element)

        sql_parts = {
            keyword: part.parse()
            for keyword, part in sql_parts.items()
        }

        return (
            sql_parts.get('select'),
            sql_parts.get('from'),
            sql_parts.get('where')
        )
