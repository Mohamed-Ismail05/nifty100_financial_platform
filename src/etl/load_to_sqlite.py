from pathlib import Path
import sqlite3
import pandas as pd

DB_PATH = Path("data/db/nifty100.db")

RAW_DATA = {
"companies": "data/raw/companies.xlsx",
"profitandloss": "data/raw/profitandloss.xlsx",
"balancesheet": "data/raw/balancesheet.xlsx",
"cashflow": "data/raw/cashflow.xlsx",
"analysis": "data/raw/analysis.xlsx",
"documents": "data/raw/documents.xlsx",
"prosandcons": "data/raw/prosandcons.xlsx",
"sectors": "data/raw/sectors.xlsx",
"stock_prices": "data/raw/stock_prices.xlsx",
"financial_ratios": "data/raw/financial_ratios.xlsx"
}

def load_excel(file_path):
    file_name = Path(file_path).name.lower()
    header_map = {"sectors.xlsx": 0,"stock_prices.xlsx": 0,"financial_ratios.xlsx": 0}
    header_row = header_map.get(file_name,1)
    return pd.read_excel(file_path,header=header_row)

def normalize_id(series):
    return (series.astype(str).str.strip().str.upper())

def log_orphans(table_name, orphan_rows):
    if len(orphan_rows) == 0:
        return
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    file_path = output_dir / "orphan_rows.csv"
    orphan_rows["source_table"] = table_name
    if file_path.exists():
        orphan_rows.to_csv(file_path,mode="a",header=False,index=False)
    else:
        orphan_rows.to_csv(file_path,index=False)

def insert_table(conn, table_name, dataframe):
    dataframe.to_sql(table_name,conn,if_exists="append",index=False)
    print(f"{table_name}: {len(dataframe)} rows inserted")

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    companies_df = load_excel(RAW_DATA["companies"])
    companies_df["id"] = normalize_id(companies_df["id"])
    valid_company_ids = set(companies_df["id"])
    try:
        insert_table(conn,"companies",companies_df)
        child_tables = [
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
        for table_name in child_tables:
            file_path = RAW_DATA[table_name]
            if not Path(file_path).exists():
                print(f"Skipped: {file_path}")
                continue
            df = load_excel(file_path)
            if "company_id" in df.columns:
                df["company_id"] = normalize_id(df["company_id"])
                orphan_rows = df[~df["company_id"].isin(valid_company_ids)].copy()
                if len(orphan_rows) > 0:
                    print(f"{table_name}: "f"{len(orphan_rows)} orphan rows removed")
                    log_orphans(table_name,orphan_rows)
                df = df[df["company_id"].isin(valid_company_ids)]
            insert_table(conn,table_name,df)
        conn.commit()
        print("\nData loading completed successfully.")
    except Exception as error:
        conn.rollback()
        print(f"\nLoad failed: {error}")
    finally:
        conn.close()
if __name__ == "__main__":
    main()
