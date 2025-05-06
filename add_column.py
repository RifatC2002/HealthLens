import sqlite3
import os

# Set the correct relative path
db_path = os.path.join("instance", "database.db")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if 'routine' column already exists
    cursor.execute("PRAGMA table_info(mood);")
    columns = [col[1] for col in cursor.fetchall()]
    if 'routine' not in columns:
        cursor.execute("ALTER TABLE mood ADD COLUMN routine TEXT;")
        print("Column 'routine' added successfully.")
    else:
        print("Column 'routine' already exists.")

    conn.commit()
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
