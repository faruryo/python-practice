import pymysql.cursors
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host", type=str)
    parser.add_argument("user", type=str)
    parser.add_argument("password", type=str)
    parser.add_argument("db", type=str)

    args = parser.parse_args()

    conn = pymysql.connect(
        host=args.host,
        user=args.user,
        db=args.db,
        password=args.password,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

    try:
        with conn.cursor() as cursor:
            cursor.execute("SHOW VARIABLES LIKE 'sql_log_bin';")
            print(cursor.fetchall())
            cursor.execute("SET sql_log_bin = OFF;")
            cursor.execute("SHOW VARIABLES LIKE 'sql_log_bin';")
            print(cursor.fetchall())

        with conn.cursor() as cursor:
            sql = "INSERT INTO product (id, name, col) VALUES (%s, %s, %s)"
            param = []
            for i in range(10):
                param.append((i, f"faru{i}", "col"))
            cursor.executemany(sql, param)
            cursor.execute("SHOW VARIABLES LIKE 'sql_log_bin';")
            print(cursor.fetchall())

        # コミットしないとロールバックされる
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    main()
