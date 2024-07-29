import create_table, fetch_and_store

try:
    create_table.run()
    fetch_and_store.upsert_valid_krx_items()
except Exception as e:
    print(f"Error: {e}")
