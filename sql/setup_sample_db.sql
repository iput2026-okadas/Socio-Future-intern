-- ============================================================
-- MySQL Backup Tool - Sample Database Setup
--
-- サンプルデータベースを作成します。
--
-- 作成されるもの:
--   Database: backup_test
--   Tables:
--     - users
--     - orders
--
-- テストデータには以下を含みます。
--   - 日本語
--   - NULL
--   - 空文字
--   - カンマ
--   - ダブルクォート
--   - 改行
--   - DATE
--   - DATETIME(6)
--   - DECIMAL
--   - JSON
--   - Foreign Key
-- ============================================================


-- ------------------------------------------------------------
-- 既存DBがあれば削除
-- ------------------------------------------------------------

DROP DATABASE IF EXISTS backup_test;


-- ------------------------------------------------------------
-- Database作成
-- ------------------------------------------------------------

CREATE DATABASE backup_test
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_0900_ai_ci;

USE backup_test;


-- ------------------------------------------------------------
-- users
-- ------------------------------------------------------------

CREATE TABLE users (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    birthday DATE NULL,
    score DECIMAL(10, 2) NULL,
    profile TEXT NULL,
    created_at DATETIME(6) NOT NULL,
    note VARCHAR(255) NULL,

    PRIMARY KEY (id),
    UNIQUE KEY uq_users_email (email)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = '利用者テーブル';


-- ------------------------------------------------------------
-- orders
--
-- users.id を Foreign Key として参照します。
-- そのため、リストア時には users を先に作成する必要があります。
-- ------------------------------------------------------------

CREATE TABLE orders (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    metadata JSON NULL,
    created_at DATETIME NOT NULL,

    PRIMARY KEY (id),
    KEY idx_orders_user_id (user_id),

    CONSTRAINT fk_orders_user
        FOREIGN KEY (user_id)
        REFERENCES users (id)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci
COMMENT = '注文テーブル';


-- ------------------------------------------------------------
-- users test data
-- ------------------------------------------------------------

INSERT INTO users (
    name,
    email,
    birthday,
    score,
    profile,
    created_at,
    note
)
VALUES
(
    '田中 太郎',
    'tanaka@example.com',
    '2000-01-01',
    92.50,
    CONCAT('1行目', CHAR(10), '2行目'),
    '2026-09-01 09:00:00.123456',
    NULL
),
(
    '鈴木 "花子"',
    'suzuki@example.com',
    NULL,
    80.00,
    '東京, 横浜',
    '2026-09-01 09:05:10.654321',
    ''
),
(
    '佐藤 次郎',
    'sato@example.com',
    '1998-05-15',
    NULL,
    '通常のプロフィール',
    '2026-09-01 10:30:00.000001',
    '備考あり'
);


-- ------------------------------------------------------------
-- orders test data
-- ------------------------------------------------------------

INSERT INTO orders (
    user_id,
    product_name,
    price,
    metadata,
    created_at
)
VALUES
(
    1,
    'ノート',
    500.00,
    JSON_OBJECT(
        'color', 'blue',
        'count', 2
    ),
    '2026-09-01 11:00:00'
),
(
    1,
    'ペン "太字"',
    120.00,
    JSON_OBJECT(
        'color', 'black'
    ),
    '2026-09-01 11:05:00'
),
(
    2,
    '定規, 30cm',
    300.00,
    NULL,
    '2026-09-01 11:10:00'
);


-- ------------------------------------------------------------
-- 確認用
-- ------------------------------------------------------------

SELECT '=== users ===' AS message;

SELECT
    id,
    name,
    email,
    birthday,
    score,
    profile,
    created_at,
    note
FROM users
ORDER BY id;


SELECT '=== orders ===' AS message;

SELECT
    id,
    user_id,
    product_name,
    price,
    metadata,
    created_at
FROM orders
ORDER BY id;


-- ------------------------------------------------------------
-- 件数確認
-- ------------------------------------------------------------

SELECT
    'users' AS table_name,
    COUNT(*) AS row_count
FROM users

UNION ALL

SELECT
    'orders' AS table_name,
    COUNT(*) AS row_count
FROM orders;

