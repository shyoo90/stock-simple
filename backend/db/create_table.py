from db_utils import get_db_connection, table_exists, apply_schema_changes, get_desired_schema
import re



# 데이터베이스 연결 설정
conn = get_db_connection()
cur = conn.cursor()
# SQL 파일 실행
SQL_FILE_PATH = '/app/db/sql/schema.sql'

def execute_sql_file(cursor, file_path):
    with open(file_path, 'r') as file:
        sql = file.read()
        cursor.execute(sql)

def get_table_names_from_schema(file_path):
    """
    Extract table names from a schema SQL file.

    Args:
        file_path (str): The path to the schema SQL file.

    Returns:
        list: A list of table names.
    """
    table_names = []
    create_table_pattern = re.compile(r'CREATE TABLE IF NOT EXISTS (\w+)', re.IGNORECASE)

    with open(file_path, 'r') as file:
        for line in file:
            match = create_table_pattern.search(line)
            if match:
                table_names.append(match.group(1))

    return table_names

def run():
    try:
        table_names = get_table_names_from_schema(SQL_FILE_PATH)
        desired_schemas = get_desired_schema(SQL_FILE_PATH)
        print("desired_schemas",desired_schemas)
        for table_name in table_names:
            if table_exists(cur, table_name):
                apply_schema_changes(cur, desired_schemas, table_name)
            else:
                execute_sql_file(cur, SQL_FILE_PATH)
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()