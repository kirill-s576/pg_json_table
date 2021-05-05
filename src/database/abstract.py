from src.lib import SingletonAbcMeta
from abc import ABC, abstractmethod


class AbstractSqlQuery(ABC):

    @property
    @abstractmethod
    def sql_query(self):
        """
        SQL query string
        :return:
        """
        pass


class AbstractConnection(metaclass=SingletonAbcMeta):
    """

    """

    __connection = None
    cursor = None

    def __init__(self,
                 host: str,
                 port: str,
                 db_name: str,
                 user: str,
                 password: str):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.user = user
        self.password = password
        self._check_database()

    @abstractmethod
    def _check_database(self):
        """
        Create database if not exists
        :return:
        """
        pass

    @abstractmethod
    def open_connection(self) -> None:
       """
       Method should attributes connection & cursor to working objects.
       :return: None
       """
       pass

    @abstractmethod
    def close_connection(self):
        """
        Method should close connection and set connection & cursor to None
        :return: None
        """
        pass

    @abstractmethod
    def send_query(self, query: AbstractSqlQuery):
        """
        Method should execute query in DB and return cursor
        :return: Cursor object.
        """
        pass

    def __enter__(self):
        """
        Open connection on enter
        """
        if not self.__connection:
            self.open_connection()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close connection on exit
        """
        if self.__connection:
            self.close_connection()

    def __del__(self):
        """
        Close connection on destroy object
        """
        if self.__connection:
            self.close_connection()


class AbstractDatabaseTable(ABC):

    def __init__(self, connection: AbstractConnection):
        self.connection = connection
        self.name = self.__class__.__name__.lower()
        self._check_table()

    @abstractmethod
    def _check_table(self):
        """
        Create table if not exists
        :return:
        """

    @abstractmethod
    def insert_row(self, **kwargs):
        """
        Insert new row in database
        :param kwargs: attributes for new row.
        :return:
        """