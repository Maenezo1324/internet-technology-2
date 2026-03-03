import psycopg2

def load_massive_csv():
    """
    Оптимизированная загрузка 20 GB CSV в PostgreSQL.
    Использует нативную команду COPY для загрузки данных потоком (минуя RAM),
    что работает на порядок быстрее стандартных INSERT INTO.
    """
    db_config = {
        "dbname": "homecredit_db",
        "user": "postgres",
        "password": "password",
        "host": "localhost",
        "port": "5432"
    }

    try:
        # Устанавливаем соединение с БД
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Создаем таблицу, если ее нет
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS letter_stats (
                letter VARCHAR(5),
                frequency BIGINT,
                percentage NUMERIC(5, 2)
            );
        """)
        
        # Очищаем таблицу перед импортом
        cursor.execute("TRUNCATE TABLE letter_stats;")

        # SQL команда COPY (берет данные прямо из потока STDIN)
        copy_sql = """
            COPY letter_stats (letter, frequency, percentage) 
            FROM STDIN WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',');
        """

        print("Начинаем загрузку 20 ГБ CSV файла в PostgreSQL...")
        
        # Открываем огромный файл как генератор, чтобы не забивать ОЗУ
        with open('massive_data.csv', 'r', encoding='utf-8') as f:
            # Метод copy_expert передает поток файла напрямую движку PostgreSQL
            cursor.copy_expert(sql=copy_sql, file=f)
            
        conn.commit()
        print("Загрузка 20 ГБ файла успешно завершена!")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_massive_csv()