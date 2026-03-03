-- Диалект: PostgreSQL

-- ==============================================================================
-- 1. На каждый день количество просмотров по SVOD и AVOD на платформах 10 и 11
-- за последние 30 дней.
-- ==============================================================================
SELECT 
    DATE(cw.show_date) AS watch_date,
    c.paid_type,
    COUNT(cw.watch_id) AS views_count
FROM content_watch cw
JOIN content c ON cw.content_id = c.content_id
WHERE cw.platform IN (10, 11)
  AND c.paid_type IN ('SVOD', 'AVOD')
  AND cw.show_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY 1, 2
ORDER BY 1 DESC, 2;


-- ==============================================================================
-- 2. Ежемесячный ТОП-5 сериалов и ТОП-5 единичного контента по кол-ву уникальных зрителей.
-- ==============================================================================
WITH MonthlyStats AS (
    SELECT 
        DATE_TRUNC('month', cw.show_date) AS watch_month,
        -- Если compilation_id IS NOT NULL, это сериал, иначе единичный фильм
        CASE WHEN c.compilation_id IS NOT NULL THEN 'Series' ELSE 'Movie' END AS content_type,
        -- ID сериала или фильма
        COALESCE(c.compilation_id, c.content_id) AS item_id, 
        COUNT(DISTINCT cw.user_id) AS unique_viewers
    FROM content_watch cw
    JOIN content c ON cw.content_id = c.content_id
    GROUP BY 1, 2, 3
),
RankedStats AS (
    SELECT 
        watch_month,
        content_type,
        item_id,
        unique_viewers,
        -- Ранжируем внутри каждого месяца и типа контента
        ROW_NUMBER() OVER(PARTITION BY watch_month, content_type ORDER BY unique_viewers DESC) as rnk
    FROM MonthlyStats
)
SELECT watch_month, content_type, item_id, unique_viewers
FROM RankedStats
WHERE rnk <= 5
ORDER BY watch_month DESC, content_type, rnk;


-- ==============================================================================
-- 3. Пользователи, у которых вчера organic сразу сменился на referral.
-- ==============================================================================
WITH YesterdayViews AS (
    SELECT 
        user_id,
        utm_medium,
        show_date,
        -- Получаем источник СЛЕДУЮЩЕГО просмотра этого же пользователя
        LEAD(utm_medium) OVER(PARTITION BY user_id ORDER BY show_date) as next_medium
    FROM content_watch
    WHERE DATE(show_date) = CURRENT_DATE - INTERVAL '1 day'
)
SELECT DISTINCT user_id
FROM YesterdayViews
WHERE utm_medium = 'organic' AND next_medium = 'referral';