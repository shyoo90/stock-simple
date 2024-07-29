import psycopg2
import os
from typing import List, Dict

class StockInfoDAO:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(StockInfoDAO, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.connection = None

    def get_db_connection(self):
        if self.connection is None:
            self.connection = psycopg2.connect(
                host="db",  # docker-compose 서비스 이름
                database=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD")
            )
        return self.connection

    def fetch_stock_info(self) -> List[Dict]:
        """
        Fetch all stock information from the database.

        Returns:
            List[Dict]: A list of dictionaries containing stock information.
        """
        with self.get_db_connection() as connection:
            with connection.cursor() as cursor:
                query = """
                    SELECT short_code, isin_code, market_category, item_name, corporate_number, corporate_name
                    FROM stock_info
                """
                cursor.execute(query)
                rows = cursor.fetchall()

                columns = ["short_code", "isin_code", "market_category", "item_name", "corporate_number", "corporate_name"]
                stock_info = [dict(zip(columns, row)) for row in rows]
                return stock_info
            
    def search_stock_info(self, query: str) -> List[Dict]:
        """
        Search stock information by query.

        Args:
            query (str): The search query.

        Returns:
            List[Dict]: A list of dictionaries containing stock information.
        """
        with self.get_db_connection() as connection:
            with connection.cursor() as cursor:
                search_query = f"%{query}%"
                query = """
                    SELECT short_code, isin_code, market_category, item_name, corporate_number, corporate_name
                    FROM stock_info
                    WHERE short_code ILIKE %s OR isin_code ILIKE %s OR market_category ILIKE %s OR item_name ILIKE %s OR corporate_number ILIKE %s OR corporate_name ILIKE %s
                """
                cursor.execute(query, (search_query, search_query, search_query, search_query, search_query, search_query))
                rows = cursor.fetchall()

                columns = ["short_code", "isin_code", "market_category", "item_name", "corporate_number", "corporate_name"]
                stock_info = [dict(zip(columns, row)) for row in rows]
                return stock_info

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
