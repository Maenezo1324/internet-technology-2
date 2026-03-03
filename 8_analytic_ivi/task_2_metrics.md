# Задание 2: Оценка продуктовых метрик

## 1. Оценка "Цепляемости" (Stickiness) и "Крутости" сериала

**Предлагаемая метрика:** Конверсия в досматриваемость (Completion Rate) от первой серии к N-ой (например, к третьей). Если 100 человек начали смотреть 1-ю серию, а до 3-й дошли 80, то сериал обладает высокой "цепляемостью". Дополнительно можно оценивать Binge-watching rate (процент пользователей, посмотревших 3 серии за одну сессию).

**Ограничения текущей базы (чего не хватает):**
В таблице `content_watch` есть поле `show_duration` (время просмотра), но в таблице `content` нет поля `total_duration` (общей длины видео). Из-за этого мы не можем отличить пользователя, который включил серию на 10 секунд и выключил, от того, кто посмотрел ее до конца. Для точного расчета нужен процент досмотра (например, `show_duration / total_duration > 0.8`).

**SQL-запрос (Расчет конверсии из 1-й серии в 3-ю):**
```sql
WITH Ep1_Viewers AS (
    SELECT DISTINCT cw.user_id, c.compilation_id
    FROM content_watch cw 
    JOIN content c ON cw.content_id = c.content_id
    WHERE c.episode = 1
),
Ep3_Viewers AS (
    SELECT DISTINCT cw.user_id, c.compilation_id
    FROM content_watch cw 
    JOIN content c ON cw.content_id = c.content_id
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
```

# **Ретеншн (Retention) пользователей и сегментация**

Предлагаемая метрика: Когортный Retention по месяцам. Аудиторию логично просегментировать по модели монетизации (AVOD, SVOD, TVOD) или по платформе (Web, SmartTV, Mobile), так как паттерны потребления контента там кардинально отличаются.

Ограничения текущей базы (чего не хватает):
Отсутствует таблица пользователей (users) с датой регистрации (registration_date) или датой начала подписки (subscription_start_date). Сейчас мы вынуждены считать когортой месяц первого просмотра в доступных логах, что искажает данные для старых пользователей (мы можем принять их за новых).

## SQL-запрос (Monthly Retention с сегментацией по платформе):

WITH UserCohorts AS (
    -- Определяем месяц первого просмотра пользователя и его основную платформу
    SELECT 
        user_id,
        MIN(DATE_TRUNC('month', show_date)) as cohort_month,
        MIN(platform) as primary_platform 
    FROM content_watch
    GROUP BY user_id
),
Activity AS (
    -- Собираем все месяцы активности пользователей
    SELECT DISTINCT user_id, DATE_TRUNC('month', show_date) as activity_month
    FROM content_watch
)
SELECT 
    uc.primary_platform,
    uc.cohort_month,
    EXTRACT(MONTH FROM age(a.activity_month, uc.cohort_month)) as month_number,
    COUNT(DISTINCT uc.user_id) as users_count
FROM UserCohorts uc
JOIN Activity a ON uc.user_id = a.user_id
GROUP BY 1, 2, 3
ORDER BY 1, 2, 3;