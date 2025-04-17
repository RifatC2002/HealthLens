import sqlite3

# Replace with your actual database path
conn = sqlite3.connect('instance/lifestyle.db')  
cursor = conn.cursor()

# Add the missing columns
try:
    cursor.execute("ALTER TABLE goal ADD COLUMN priority TEXT DEFAULT 'Medium'")
except sqlite3.OperationalError:
    print("Column 'priority' already exists")

try:
    cursor.execute("ALTER TABLE goal ADD COLUMN completion BOOLEAN DEFAULT 0")
except sqlite3.OperationalError:
    print("Column 'completion' already exists")

conn.commit()
conn.close()
print("Migration complete.")
