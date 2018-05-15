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
    def from_string(column_string):


        pass

    def __init__(self, table, column):
        pass


class Condition():

    @classmethod
    def from_string(condition_string):
        pass

    def __init__(self, compared, comparee, sign):
        pass


class Source():

    @classmethod
    def from_string(source_string):
        pass

    def __init__(self, table):
        pass


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
        if element != self.SEPARATOR:
            self.raw_elements.append(element)

    def parse(self):
        return self.PARSED_ENTITY.from_string(self.parsed_elements)


class Select(SqlPart):

    SEPARATOR = ','


class From(SqlPart):

    KEYWORD = 'from'


class Where(SqlPart):

    KEYWORD = 'where'
    SEPRATOR = 'and'


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
