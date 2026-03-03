-- ЗАПРОС 1: Заказы пользователей (> 10 заказов)
SELECT user_id, COUNT(*) as total_orders
FROM orders
GROUP BY user_id
HAVING COUNT(*) > 10;
-- Пояснение: Используем агрегацию по индексированному полю user_id.

-- ЗАПРОС 2: Средний чек за последний месяц
SELECT user_id, AVG(total_price) as avg_order_value
FROM orders
WHERE created_at >= NOW() - INTERVAL '1 month'
GROUP BY user_id;
-- Пояснение: Фильтрация по времени перед группировкой отсекает лишние данные.

-- ЗАПРОС 3: Сравнение среднего чека Year-over-Year (Текущий год vs Прошлый)
WITH monthly_stats AS (
    SELECT 
        EXTRACT(YEAR FROM created_at) as year,
        EXTRACT(MONTH FROM created_at) as month,
        AVG(total_price) as avg_price
    FROM orders
    WHERE created_at >= date_trunc('year', NOW() - INTERVAL '1 year')
    GROUP BY 1, 2
)
SELECT 
    curr.month,
    curr.avg_price as avg_this_year,
    prev.avg_price as avg_last_year
FROM monthly_stats curr
JOIN monthly_stats prev ON curr.month = prev.month 
    AND curr.year = EXTRACT(YEAR FROM NOW())
    AND prev.year = EXTRACT(YEAR FROM NOW()) - 1;