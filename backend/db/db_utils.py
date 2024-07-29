import psycopg2
import os
import re
def get_db_connection():
    conn = psycopg2.connect(
        host="db",  # docker-compose 서비스 이름
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    return conn



def table_exists(cursor, table_name):
    """
    Check if a table exists in the database.

    Args:
        cursor: The database cursor.
        table_name (str): The name of the table to check.

    Returns:
        bool: True if the table exists, False otherwise.
    """
    cursor.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_name = %s
    );
    """, (table_name,))
    return cursor.fetchone()[0]

def get_current_schema(cursor, table_name):
    """
    Get the current schema of a table.

    Args:
        cursor: The database cursor.
        table_name (str): The name of the table.

    Returns:
        dict: A dictionary containing the current schema of the table.
    """
    cursor.execute(f"""
    SELECT column_name, data_type, is_nullable, column_default
    FROM information_schema.columns
    WHERE table_name = %s;
    """, (table_name,))
    
    schema = {}
    for row in cursor.fetchall():
        column_name, data_type, is_nullable, column_default = row
        schema[column_name] = {
            'data_type': data_type,
            'is_nullable': 'NO' if is_nullable == 'NO' else 'YES',
            'column_default': column_default
        }
    return schema

def get_desired_schema(sql_file_path):
    """
    Parse the desired schema from the SQL file.

    Args:
        sql_file_path (str): The path to the SQL file containing the desired schema.

    Returns:
        dict: A dictionary containing the desired schema for each table.
    """
    schemas = {}
    table_name = None
    table_start_pattern = re.compile(r'CREATE TABLE IF NOT EXISTS (\w+) \(', re.IGNORECASE)
    table_end_pattern = re.compile(r'\);')

    with open(sql_file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip().strip(',')
            match_start = table_start_pattern.match(line)
            if match_start:
                table_name = match_start.group(1)
                schemas[table_name] = {}
                continue
            if table_name and table_end_pattern.match(line):
                table_name = None
                continue
            if table_name:
                parts = re.split(r'\s+', line, maxsplit=2)
                if len(parts) < 2:
                    continue
                
                column_name, data_type = parts[0], parts[1].lower()  # Convert to lowercase for consistency
                if column_name=="UNIQUE":
                    continue
                is_nullable = 'NO' if 'NOT NULL' in line else 'YES'
                column_default = None
                if 'DEFAULT' in line:
                    match = re.search(r'DEFAULT\s+(\S+)', line)
                    if match:
                        column_default = match.group(1)
                if "varchar" in data_type:
                    data_type = 'character varying'
                if "timestamp" in data_type:
                    data_type = 'timestamp without time zone'
                schemas[table_name][column_name] = {
                    'data_type': data_type,
                    'is_nullable': is_nullable,
                    'column_default': column_default
                }
    return schemas

def apply_schema_changes(cursor, desired_schemas, table_name):
    """
    Apply schema changes to the specified table.

    Args:
        cursor: The database cursor.
        sql_file_path (str): The path to the SQL file containing the desired schema.
        table_name (str): The name of the table to modify or create.
    """
    desired_schema = desired_schemas.get(table_name)
    if desired_schema==None:
        return
    current_schema = get_current_schema(cursor, table_name)

    print("============")
    print("desired_schema", desired_schema)
    print("============")
    print("current_schema", current_schema)
    print("============")
    
    for column, properties in desired_schema.items():
        if column=='id':
            continue
        if column not in current_schema:
            # Create column with appropriate properties
            column_def = f"{column} {properties['data_type']}"
            if properties['is_nullable'] == 'NO':
                column_def += " NOT NULL"
            if properties['column_default'] is not None:
                column_def += f" DEFAULT {properties['column_default']}"
            sql = f"ALTER TABLE {table_name} ADD COLUMN {column_def};"
            print(1, sql)
            cursor.execute(sql)
        else:
            # Check for property changes
            if current_schema[column]['data_type'] != properties['data_type']:
                sql = f"ALTER TABLE {table_name} ALTER COLUMN {column} TYPE {properties['data_type']};"
                print(2, sql)
                cursor.execute(sql)
            if current_schema[column]['is_nullable'] != properties['is_nullable']:
                null_action = "DROP NOT NULL" if properties['is_nullable'] == 'YES' else "SET NOT NULL"
                sql = f"ALTER TABLE {table_name} ALTER COLUMN {column} {null_action};"
                print(3, sql)
                cursor.execute(sql)
            if current_schema[column]['column_default'] != properties['column_default']:
                if properties['column_default'] is None:
                    sql = f"ALTER TABLE {table_name} ALTER COLUMN {column} DROP DEFAULT;"
                else:
                    sql = f"ALTER TABLE {table_name} ALTER COLUMN {column} SET DEFAULT {properties['column_default']};"
                print(4, sql)
                cursor.execute(sql)

