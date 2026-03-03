# Продуктовые метрики (Задание 2)

## 1. Метрика "Цепляемость" сериала
**Идея:** Основная метрика "крутости" сериала на старте — это **Completion Rate (Конверсия в досматриваемость)** от первой серии к N-ой (например, к третьей). Если 100 человек начали смотреть 1 серию, а до 3-й дошли 80, то сериал отлично "цепляет".

**Чего не хватает в данных:**
Поле `show_duration` указывает время просмотра в секундах, но в таблице `content` нет поля `total_duration` (общей длины видео). Без него мы не можем отличить пользователя, который посмотрел 10 секунд и выключил, от того, кто посмотрел серию целиком.

**SQL-запрос (Конверсия из 1-й серии в 3-ю):**
```sql
WITH Ep1_Viewers AS (
    SELECT DISTINCT cw.user_id, c.compilation_id
    FROM content_watch cw JOIN content c ON cw.content_id = c.content_id
    WHERE c.episode = 1
),
Ep3_Viewers AS (
    SELECT DISTINCT cw.user_id, c.compilation_id
    FROM content_watch cw JOIN content c ON cw.content_id = c.content_id
    WHERE c.episode = 3
)
SELECT 
    e1.compilation_id,
    COUNT(DISTINCT e1.user_id) as started_ep1,
    COUNT(DISTINCT e3.user_id) as reached_ep3,
    ROUND(COUNT(DISTINCT e3.user_id)::numeric / NULLIF(COUNT(DISTINCT e1.user_id), 0) * 100, 2) as stickiness_percent
FROM Ep1_Viewers e1
LEFT JOIN Ep3_Viewers e3 ON e1.user_id = e3.user_id AND e1.compilation_id = e3.compilation_id
GROUP BY 1
ORDER BY stickiness_percent DESC;