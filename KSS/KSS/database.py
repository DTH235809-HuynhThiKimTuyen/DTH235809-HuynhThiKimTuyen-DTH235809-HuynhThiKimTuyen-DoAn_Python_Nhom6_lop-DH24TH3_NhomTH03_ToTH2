import mysql.connector

def get_connection():
    try:
        return mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='Aa@123456',  # <--- ĐIỀN MẬT KHẨU MYSQL CỦA BẠN (XAMPP thì để trống)
            database='hotel_management'
        )
    except Exception as e:
        print("Lỗi kết nối:", e)
        return None

def fetch_all(sql, params=None):
    conn = get_connection()
    if not conn: return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or ())
        return cur.fetchall()
    finally:
        conn.close()

def execute_query(sql, params=None):
    conn = get_connection()
    if not conn: return False
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        conn.commit()
        return True
    except Exception as e:
        print("Lỗi SQL:", e)
        return False
    finally:
        conn.close()

def dang_nhap(user, pwd):
    rows = fetch_all("SELECT * FROM users WHERE Username=%s AND Password=%s", (user, pwd))
    return rows[0] if rows else None