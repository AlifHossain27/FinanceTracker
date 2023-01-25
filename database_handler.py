import sqlite3


conn = sqlite3.connect("financeTracker.db")
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS DailyExpense
(id INTEGER PRIMARY KEY,
date DATE,
earn REAL,
spent REAL,
saved REAL
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS ExpenseList
(id INTEGER PRIMARY KEY,
date DATE,
category TEXT,
description TEXT,
amount REAL
)""")

conn.commit()
conn.close()