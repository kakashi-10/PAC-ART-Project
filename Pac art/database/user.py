import mysql.connector

db=mysql.connector.connect(host='localhost', user='root', password='Haimot@10')
# Tạo con trỏ để thực thi câu lệnh SQL
cursor = db.cursor()
# Tạo cơ sở dữ liệu (nếu chưa có)
cursor.execute("CREATE DATABASE IF NOT EXISTS pac_art")
# Chọn cơ sở dữ liệu
db.database = "pac_art"
# Tạo bảng
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
# Đóng con trỏ và kết nối
cursor.close()
db.close()

