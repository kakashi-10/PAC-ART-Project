import mysql.connector

db=mysql.connector.connect(host='localhost', user='root', password='Haimot@10')
# Tạo con trỏ để thực thi câu lệnh SQL
cursor = db.cursor()
# Tạo cơ sở dữ liệu (nếu chưa có)
cursor.execute("CREATE DATABASE IF NOT EXISTS pac_art")
# Chọn cơ sở dữ liệu
db.database = "pac_art"

# Tạo bảng

# user bable
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# image table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS image (
        id_image INT AUTO_INCREMENT PRIMARY KEY,
        upload_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        name_image VARCHAR(255) NOT NULL,
        image_data LONGBLOB NOT NULL,  -- Lưu trữ ảnh dưới dạng nhị phân
        user_id INT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
    )
''')

# edited_image table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS edited_image (
        edited_id_image INT AUTO_INCREMENT PRIMARY KEY,
        name_image VARCHAR(255) NOT NULL,
        image_data LONGBLOB NOT NULL,  -- Lưu trữ ảnh dưới dạng nhị phân
        user_id INT NOT NULL,
        edit_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
    )
''')

# Đóng con trỏ và kết nối
cursor.close()
db.close()