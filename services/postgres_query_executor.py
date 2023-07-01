from typing import Any

import psycopg2

from settings import POSTGRES_SERVER_HOST, POSTGRES_SERVER_PORT, POSTGRES_SERVER_USERNAME, POSTGRES_SERVER_PASSWORD, \
    POSTGRES_SERVER_DATABASE


class PostgresQueryExecutor:
    """
    A service responsible for executing a query to our postgres database server
    """
    def __init__(self):
        # Establish a database driver (or a database connector) to our local postgres database server
        self.conn = psycopg2.connect(
            host=POSTGRES_SERVER_HOST,
            port=POSTGRES_SERVER_PORT,
            database=POSTGRES_SERVER_DATABASE,
            user=POSTGRES_SERVER_USERNAME,
            password=POSTGRES_SERVER_PASSWORD
        )
        # A postgres Cursor object, used to execute a query
        self.cursor = self.conn.cursor()

    def execute(self, query: str) -> list[tuple[Any]]:
        self.cursor.execute(query)
        results: list[tuple[Any]] = self.cursor.fetchall()
        # for debugging what type the results are
        # print(f"results: {results}, type: {type(results)}, {type(results[0])}")
        self.conn.commit()
        return results

POSTGRESQL_QUERY_EXECUTOR: PostgresQueryExecutor = PostgresQueryExecutor()


if __name__ == "__main__":
    query_executor: PostgresQueryExecutor = PostgresQueryExecutor()
    sql_query: str = """
SELECT * FROM usage_data;
"""
    """
    results: [(1, 1, datetime.date(2020, 1, 1), datetime.time(8, 0), datetime.timedelta(seconds=3600)), (2, 1, datetime.date(2020, 1, 2), datetime.time(8, 0), datetime.timedelta(seconds=7200)), (3, 2, datetime.date(2020, 2, 1), datetime.time(8, 0), datetime.timedelta(seconds=10800))], type: <class 'list'>
    """
    result = query_executor.execute(sql_query)
    print(result)