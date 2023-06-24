import sqlite3

import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect("attendance.db")

# Retrieve the data from the 'students' table and sort it by 'usn'
query = "SELECT * FROM students ORDER BY usn"
df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Save the sorted data to an Excel file
df.to_excel("students_sorted.xlsx", index=False)
