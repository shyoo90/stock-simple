from typing import List, Dict
from pydantic import BaseModel

class StockInfo(BaseModel):
    short_code: str
    isin_code: str
    market_category: str
    item_name: str
    corporate_number: str
    corporate_name: str

# 주식 데이터 모델
class StockItem(BaseModel):
    basDt: str
    srtnCd: str
    isinCd: str
    itmsNm: str
    mrktCtg: str
    clpr: str
    vs: str
    fltRt: str
    mkp: str
    hipr: str
    lopr: str
    trqu: str
    trPrc: str
    lstgStCnt: str
    mrktTotAmt: str