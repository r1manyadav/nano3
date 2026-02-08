import sqlite3
import json
import os

# Use absolute path to database in instance folder
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BACKEND_DIR, 'instance', 'nano_test_platform.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]

print("\n" + "="*80)
print("NANO TEST PLATFORM - DATABASE CONTENTS")
print("="*80 + "\n")

for table_name in tables:
    print(f"\n{'='*80}")
    print(f"TABLE: {table_name.upper()}")
    print(f"{'='*80}")
    
    # Get table schema
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    
    # Print column info
    print(f"\nColumns: {', '.join(column_names)}\n")
    
    # Get all records
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    
    if len(rows) == 0:
        print("(No records)\n")
    else:
        print(f"Total Records: {len(rows)}\n")
        # Print first few records
        for i, row in enumerate(rows[:5]):  # Show first 5
            print(f"Record {i+1}:")
            for j, col_name in enumerate(column_names):
                value = row[j]
                # Truncate long values
                if isinstance(value, str) and len(value) > 50:
                    value = value[:47] + "..."
                print(f"  {col_name}: {value}")
            print()
        
        if len(rows) > 5:
            print(f"... and {len(rows) - 5} more records\n")

print("\n" + "="*80)
print("DATABASE SUMMARY")
print("="*80)
for table_name in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    count = cursor.fetchone()[0]
    print(f"✓ {table_name}: {count} records")

conn.close()
print("\n✓ Database file location: instance/nano_test_platform.db")
