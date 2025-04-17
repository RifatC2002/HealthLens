
import sqlite3

# Update path to your actual DB
conn = sqlite3.connect('instance/database.db')
cursor = conn.cursor()

# Add `priority` column if not exists
try:
    cursor.execute("ALTER TABLE goal ADD COLUMN priority TEXT DEFAULT 'Medium'")
    print("Added 'priority' column.")
except sqlite3.OperationalError:
    print("Column 'priority' already exists.")

# Add `completion` column if not exists
try:
    cursor.execute("ALTER TABLE goal ADD COLUMN completion BOOLEAN DEFAULT 0")
    print("Added 'completion' column.")
except sqlite3.OperationalError:
    print("Column 'completion' already exists.")

conn.commit()
conn.close()
print("Migration complete.")
