-- 테이블 생성 쿼리
CREATE TABLE IF NOT EXISTS stock_info (
    id SERIAL PRIMARY KEY,
    short_code VARCHAR(10) NOT NULL UNIQUE,
    isin_code VARCHAR(20) NOT NULL UNIQUE,
    market_category VARCHAR(10) NOT NULL,
    item_name VARCHAR(255) NOT NULL UNIQUE,
    corporate_number VARCHAR(20) NOT NULL,
    corporate_name VARCHAR(255) NOT NULL,
    create_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);