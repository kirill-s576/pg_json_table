import psycopg2
from abc import abstractmethod
from src.database.abstract import (
    AbstractSqlQuery,
    AbstractConnection,
    AbstractDatabaseTable
)


class PostgresSqlQuery(AbstractSqlQuery):
    """

    """
    @property
    @abstractmethod
    def vars(self):
        """
        Bound vars for executing query
        :return:
        """
        pass


class PostgresSimpleQuery(PostgresSqlQuery):

    def __init__(self, query, bound_vars=None):
        self.query = query
        self.bound_vars = bound_vars

    @property
    def sql_query(self):
        return self.query

    @property
    def vars(self):
        return self.bound_vars


class PostgresConnection(AbstractConnection):
    """

    """

    def _check_database(self):
        """
        Create database if not exists.
        """
        postgres_create_db_query = \
        f"""
        SELECT 'CREATE DATABASE {self.db_name}'\
        WHERE NOT EXISTS\
        (SELECT FROM pg_database WHERE datname = '{self.db_name}')
        """
        query = PostgresSimpleQuery(postgres_create_db_query, None)
        self.open_connection()
        self.send_query(query)
        self.close_connection()

    def open_connection(self):
        self.__connection = psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            dbname=self.db_name
        )
        self.cursor = self.__connection.cursor()

    def close_connection(self):
        self.cursor.close()
        self.__connection.close()

    def send_query(self, query: PostgresSqlQuery):
        self.cursor.execute(query.sql_query, query.vars)
        self.__connection.commit()
        return self.cursor


class PostgresTable(AbstractDatabaseTable):

    def __init__(self, connection: PostgresConnection):
        """
        Reimplemented __init__ for connection type hinting.
        :param connection: PostgresConnection -
        :param table_name:
        """
        super().__init__(connection)

    @abstractmethod
    def _check_table(self):
        """
        Create table if not exists
        This method must be reimplemented in concrete table
        :return:
        """
        pass

    @abstractmethod
    def insert_row(self, **kwargs):
        """
        Insert new row in database
        This method must be reimplemented in concrete table
        :param kwargs: attributes for new row.
        :return:
        """
        pass