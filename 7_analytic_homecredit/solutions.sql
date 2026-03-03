-- ==========================================
-- ЗАДАНИЕ 1: Удаление дубликатов
-- ==========================================
-- Оптимально: Использование оконной функции ROW_NUMBER(). 
-- Это позволяет за один проход пронумеровать дубли и удалить все, кроме первого (где rn = 1).
DELETE FROM your_table
WHERE id IN (
    SELECT id
    FROM (
        SELECT id, ROW_NUMBER() OVER (PARTITION BY dup_col1, dup_col2 ORDER BY id) as rn
        FROM your_table
    ) t
    WHERE t.rn > 1
);


-- ==========================================
-- ЗАДАНИЕ 2: Контроль операций (10+ млн записей)
-- ==========================================
-- Оптимально: Использование LEAD() вместо самообъединения (JOIN таблицы самой на себя), 
-- что исключает квадратичную сложность и работает за один проход (Full Table Scan).
INSERT INTO target_control_table (tOper, tControl)
SELECT tOper, tControl
FROM (
    SELECT 
        tOper,
        LEAD(tOper) OVER (ORDER BY tOper) as tControl,
        requires_control
    FROM Operations
) subquery
WHERE requires_control = true AND tControl IS NOT NULL;


-- ==========================================
-- ЗАДАНИЕ 3: Поиск счетов по секциям (миллиард строк)
-- ==========================================
-- Оптимально: Написание PL/pgSQL функции с динамическим SQL (EXECUTE). 
-- Обращаемся напрямую к нужной таблице (например, Accounts_01), минуя тяжеловесное представление (VIEW).
CREATE OR REPLACE FUNCTION get_client_accounts(
    p_bank_num TEXT, 
    p_fio TEXT, 
    p_dbirth DATE
)
RETURNS TABLE(account TEXT) AS $$
BEGIN
    RETURN QUERY EXECUTE format(
        'SELECT account FROM Accounts_%s WHERE FIO = $1 AND dBirth = $2', 
        p_bank_num
    ) USING p_fio, p_dbirth;
END;
$$ LANGUAGE plpgsql;


-- ==========================================
-- ЗАДАНИЕ 4: Сбор дат рождения из двух таблиц
-- ==========================================
-- Оптимально: Использование FULL OUTER JOIN для объединения клиентов из обеих таблиц, 
-- и COALESCE для выбора первого непустого значения даты рождения.
SELECT 
    COALESCE(c1.id, c2.id) AS id,
    COALESCE(c1.dBirth, c2.dBirth) AS dBirth
FROM Clients_1 c1
FULL OUTER JOIN Clients_2 c2 ON c1.id = c2.id;


-- ==========================================
-- ЗАДАНИЕ 5: Индексы для оптимизации
-- ==========================================
-- Запрос ищет строго по равенству a1.FIO = '...' AND a1.dBirth = '...'.
-- Условие left(a1.account,3) != '408' не поддается эффективной индексации через B-Tree,
-- поэтому индекс строится только по высокоселективным полям FIO и dBirth.
CREATE INDEX idx_accounts01_fio_dbirth ON Accounts_01(FIO, dBirth);
CREATE INDEX idx_accounts02_fio_dbirth ON Accounts_02(FIO, dBirth);


-- ==========================================
-- ЗАДАНИЕ 6: Запрос к 1 млрд операций
-- ==========================================
-- Оптимально: Строгая фильтрация дат по диапазону (SARGable условие).
-- НЕ используем EXTRACT(MONTH FROM o.date) = 6, так как это сломает индекс по дате.
SELECT SUM(o.amount)
FROM Clients c
JOIN Accounts a ON c.id = a.id_client
JOIN Operations o ON a.id = o.id_account
WHERE c.FIO = 'Иванов Иван Иванович' 
  AND c.dBirth = '1990-05-17'
  AND o.date >= '2020-06-01' 
  AND o.date < '2020-07-01';