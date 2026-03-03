-- Используемая БД: PostgreSQL 16

-- 1. Создание структуры
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total_price NUMERIC(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_name VARCHAR(255),
    price NUMERIC(10, 2),
    quantity INTEGER
);

-- Индексы для оптимизации
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);

-- 2. Генерация тестовых данных (по 1 млн+ строк)
-- Пользователи
INSERT INTO users (name, email, created_at)
SELECT 
    'User_' || i, 
    'user_' || i || '@example.com',
    NOW() - (random() * interval '3 years')
FROM generate_series(1, 1000000) s(i);

-- Заказы (2 млн строк)
INSERT INTO orders (user_id, total_price, created_at)
SELECT 
    floor(random() * 1000000 + 1)::int,
    (random() * 5000 + 100)::numeric(10,2),
    NOW() - (random() * interval '2 years')
FROM generate_series(1, 2000000) s(i);

-- Позиции заказов (3 млн строк)
INSERT INTO order_items (order_id, product_name, price, quantity)
SELECT 
    floor(random() * 2000000 + 1)::int,
    'Product_' || floor(random() * 100 + 1),
    (random() * 1000 + 10)::numeric(10,2),
    floor(random() * 5 + 1)::int
FROM generate_series(1, 3000000) s(i);