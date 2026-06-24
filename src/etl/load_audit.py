import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime

DB_PATH = "data/db/nifty100.db"

TABLES = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents",
    "prosandcons",
    "sectors",
    "stock_prices",
    "financial_ratios"
]

conn = sqlite3.connect(DB_PATH)
audit_rows = []
for table in TABLES:
    count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    audit_rows.append({"table_name": table,"rows_loaded": count,"timestamp": datetime.now()})
conn.close()
audit_df = pd.DataFrame(audit_rows)
Path("output").mkdir(exist_ok=True)
audit_df.to_csv("output/load_audit.csv",index=False)
print("load_audit.csv generated")