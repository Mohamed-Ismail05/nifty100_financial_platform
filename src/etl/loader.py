""" Excel file loading module. """ 

from pathlib import Path 
import pandas as pd 

def load_excel(file_path):
    """ Load Excel file using row 2 as header. """ 
    path = Path(file_path) 
    if not path.exists(): 
        raise FileNotFoundError( f"File not found: {file_path}" ) 
    return pd.read_excel( path, header=1 ) 
def preview_dataset(file_path, rows=5): 
    """ Display first few rows """ 
    df = load_excel(file_path) 
    return df.head(rows)