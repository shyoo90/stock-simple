import requests
import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta
import os

from db_utils import get_db_connection

# 데이터베이스 연결 설정
conn = get_db_connection()
cur = conn.cursor()

# API URLs and keys
STOCK_API_URL=os.getenv("STOCK_API_URL")
KRX_API_URL=os.getenv("KRX_API_URL")
API_KEY=os.getenv("API_KEY")

def fetch_data(api_url, params):
    """
    Fetch data from the specified API URL with the given parameters.
    
    Args:
    - api_url (str): The URL of the API endpoint.
    - params (dict): The parameters to be sent in the query string.
    
    Returns:
    - dict: The JSON response from the API if successful and valid.
    - None: If an exception occurs or the response is invalid.
    """
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        data = response.json()

        # Check for valid response code and non-empty items
        if data['response']['header']['resultCode'] != '00':
            print(f"Invalid response code: {data['response']['header']['resultCode']}")
            return None
        if not data['response']['body']['items']['item']:
            print("No items found in the response.")
            return None

        return data['response']['body']['items']['item']

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except KeyError as e:
        print(f"Unexpected response structure: {e}")
        return None

def get_params(api_key, base_dt=None, num_of_rows=4000, page_no=1):
    """
    Generate parameters for the API request.
    
    Args:
        api_key (str): The API key for authentication.
        base_dt (str, optional): The base date for the data request. Defaults to None.
        num_of_rows (int, optional): The number of rows to request. Defaults to 4000.
        page_no (int, optional): The page number to request. Defaults to 1.
    
    Returns:
        dict: A dictionary of parameters for the API request.
    """
    param = {
        'serviceKey': api_key,
        'resultType': 'json',
        'numOfRows': num_of_rows,
        'pageNo': page_no
    }
    if base_dt is not None:
        param['basDt'] = base_dt
    return param

def get_valid_krx_data():
    """
    Fetch valid KRX data by comparing with stock data.
    
    Returns:
        list: A list of valid KRX items.
    
    Raises:
        Exception: If the API request fails or no data is received.
    """
    base_dt_params = get_params(api_key=API_KEY, num_of_rows=1)
    stock_dt_data = fetch_data(api_url=STOCK_API_URL, params=base_dt_params)
    krx_dt_data = fetch_data(api_url=KRX_API_URL, params=base_dt_params)
    
    if not stock_dt_data or not krx_dt_data:
        raise Exception("API error: No data received")

    stock_base_dt = stock_dt_data[0]['basDt']
    krx_base_dt = krx_dt_data[0]['basDt']
    
    stock_params = get_params(api_key=API_KEY, base_dt=stock_base_dt)
    krx_params = get_params(api_key=API_KEY, base_dt=krx_base_dt)

    stock_data = fetch_data(api_url=STOCK_API_URL, params=stock_params)
    krx_data = fetch_data(api_url=KRX_API_URL, params=krx_params)

    if not stock_data or not krx_data:
        raise Exception("API error: No data received for stock or krx data")

    stock_items = {item['itmsNm'] for item in stock_data}
    valid_krx_items = [item for item in krx_data if item['itmsNm'] in stock_items]
    return valid_krx_items

def get_existing_items(cursor):
    """
    Fetch existing items from the database.

    Args:
        cursor: The database cursor.

    Returns:
        dict: A dictionary with item_name as keys and other attributes as values.
    """
    query = "SELECT item_name, short_code, isin_code, market_category, corporate_number, corporate_name FROM stock_info"
    cursor.execute(query)
    rows = cursor.fetchall()
    existing_items = {row[0]: {
        'short_code': row[1],
        'isin_code': row[2],
        'market_category': row[3],
        'corporate_number': row[4],
        'corporate_name': row[5]
    } for row in rows}
    return existing_items

def upsert_stock_info(cursor, item, existing_item=None):
    """
    Upsert stock information into the stock_info table.

    Args:
        cursor: The database cursor.
        item (dict): A dictionary containing the stock information.
        existing_item (dict): A dictionary containing the existing stock information, if any.
    """
    if existing_item:
        # Update if any attribute is different
        if (item['short_code'] != existing_item['short_code'] or
            item['isin_code'] != existing_item['isin_code'] or
            item['market_category'] != existing_item['market_category'] or
            item['corporate_number'] != existing_item['corporate_number'] or
            item['corporate_name'] != existing_item['corporate_name']):
            query = """
            UPDATE stock_info SET
                short_code = %s,
                isin_code = %s,
                market_category = %s,
                corporate_number = %s,
                corporate_name = %s,
                update_datetime = CURRENT_TIMESTAMP
            WHERE item_name = %s;
            """
            cursor.execute(query, (
                item['short_code'],
                item['isin_code'],
                item['market_category'],
                item['corporate_number'],
                item['corporate_name'],
                item['item_name']
            ))
    else:
        # Insert if the item does not exist
        query = """
        INSERT INTO stock_info (short_code, isin_code, market_category, item_name, corporate_number, corporate_name)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query, (
            item['short_code'],
            item['isin_code'],
            item['market_category'],
            item['item_name'],
            item['corporate_number'],
            item['corporate_name']
        ))

def upsert_valid_krx_items():
    """
    Upsert valid KRX items into the stock_info table.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    valid_krx_items = get_valid_krx_data()
    existing_items = get_existing_items(cur)

    try:
        for item in valid_krx_items:
            existing_item = existing_items.get(item['itmsNm'])
            upsert_stock_info(cur, {
                'short_code': item['srtnCd'],
                'isin_code': item['isinCd'],
                'market_category': item['mrktCtg'],
                'item_name': item['itmsNm'],
                'corporate_number': item['crno'],
                'corporate_name': item['corpNm']
            }, existing_item)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error during upsert: {e}")
    finally:
        cur.close()
        conn.close()


