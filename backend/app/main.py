
from fastapi import FastAPI, Depends, Query
from typing import List, Dict, Optional
from services.stock_info_service import StockInfoService
from dao.stock_info_dao import StockInfoDAO
from models.stock_info import StockInfo, StockItem
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용, 실제 배포 시에는 구체적인 도메인 지정
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)


def get_dao():
    return StockInfoDAO()

def get_service(dao: StockInfoDAO = Depends(get_dao)):
    return StockInfoService(dao)

@app.get("/stocks", response_model=List[StockInfo])
def get_stocks(query: Optional[str] = Query(None), service: StockInfoService = Depends(get_service)):
    """
    Get all stock information from the database.

    Returns:
        List[StockInfo]: A list of dictionaries containing stock information.
    """
    try:
        if query:
            stock_info = service.search_stocks(query)
        else:
            stock_info = service.get_all_stocks()
        return stock_info
    except Exception as e:
        print(f"Error fetching stock information: {e}")
        return {"error": "Failed to fetch stock information"}


# 주식 데이터 리스트
        # "response": {
        # "header": {
        #     "resultCode": "00",
        #     "resultMsg": "NORMAL SERVICE."
        # },
        # "body": {
        #     "numOfRows": 1000,
        #     "pageNo": 1,
        #     "totalCount": 704,
        #     "items": {
        #         "item": [

# with open(f"{ROOT_DIR}/vuno.json", "r") as f:
#     res_data = json.load(f)
# stock_data = res_data["response"]["body"]["items"]["item"]

# @app.post("/stocks/")
# async def add_stock_data(stock_item: List[StockItem]):
#     stock_data.extend(stock_item)
#     return {"message": "Stock data added successfully"}

# @app.get("/stocks/")
# async def get_stock_data():
#     return stock_data
