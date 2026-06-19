from src.etl.loader import load_excel 
core_files = [ "companies.xlsx", "profitandloss.xlsx", "balancesheet.xlsx", 
              "cashflow.xlsx", "analysis.xlsx", "documents.xlsx", "prosandcons.xlsx"] 
for file_name in core_files: 
    file_path = f"data/raw/{file_name}" 
    dataset = load_excel(file_path) 
    print( f"{file_name} loaded successfully!! | Rows: {dataset.shape[0]} | Columns: {dataset.shape[1]}" )