from dao.stock_info_dao import StockInfoDAO
from typing import List, Dict

class StockInfoService:
    def __init__(self, dao: StockInfoDAO):
        self.dao = dao

    def get_all_stocks(self) -> List[Dict]:
        """
        Get all stock information.

        Returns:
            List[Dict]: A list of dictionaries containing stock information.
        """
        stock_info = self.dao.fetch_stock_info()
        return stock_info
    
    def search_stocks(self, query: str) -> List[Dict]:
        """
        Search stocks by query.

        Args:
            query (str): The search query.

        Returns:
            List[Dict]: A list of dictionaries containing stock information.
        """
        stock_info = self.dao.search_stock_info(query)
        return stock_info
