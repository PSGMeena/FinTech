import pandas as pd
import io
from fastapi import UploadFile, HTTPException

async def parse_financial_file(file: UploadFile) -> pd.DataFrame:
    content = await file.read()
    filename = file.filename.lower()
    
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            df = pd.read_excel(io.BytesIO(content))
        elif filename.endswith('.pdf'):
            # Placeholder for PDF parsing logic
            # implementing PDFs requires pypdf or similar and complex logic
            raise HTTPException(status_code=400, detail="PDF parsing not fully implemented yet, please use CSV or Excel for this demo.")
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
            
        return normalize_columns(df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing file: {str(e)}")

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Remove any completely empty rows
    df = df.dropna(how='all')
    
    # Heuristic column mapping
    # We expect columns like Date, Description, Debit, Credit, Balance
    # We will try to standardize them
    
    # Convert all columns to lower case for matching
    df.columns = df.columns.astype(str).str.lower().str.strip()
    
    # --- ROBUST COLUMN MATCHING ---
    # Instead of a fixed map, we search for keywords in column names
    
    found_cols = df.columns.tolist()
    
    # 1. FIND DATE
    if 'date' not in found_cols:
        date_candidates = [c for c in found_cols if 'date' in c or 'time' in c or 'month' in c]
        if date_candidates:
            df.rename(columns={date_candidates[0]: 'date'}, inplace=True)
        else:
            # Create dummy date if absolutely missing
            df['date'] = pd.date_range(end=pd.Timestamp.now(), periods=len(df)).to_list()

    # 2. FIND DESCRIPTION (Product, Item, Narration)
    if 'description' not in found_cols:
        desc_keywords = ['description', 'narration', 'particulars', 'product', 'item', 'details', 'name', 'source', 'category']
        val = next((c for c in found_cols if any(k in c for k in desc_keywords)), None)
        if val:
            df.rename(columns={val: 'description'}, inplace=True)
        else:
            # Use the first object/string column as description
            obj_cols = df.select_dtypes(include=['object']).columns
            if len(obj_cols) > 0:
                df.rename(columns={obj_cols[0]: 'description'}, inplace=True)
            else:
                 df['description'] = "Transaction"

    # 3. FIND CREDIT (Income, Revenue, Sales, Deposit)
    if 'credit' not in found_cols:
        credit_keywords = ['credit', 'deposit', 'income', 'revenue', 'sales', 'received', 'total', 'gross']
        val = next((c for c in found_cols if any(k in c for k in credit_keywords)), None)
        if val:
            df.rename(columns={val: 'credit'}, inplace=True)
    
    # 4. FIND DEBIT (Expense, Cost, Withdrawal, Payment)
    if 'debit' not in found_cols:
         debit_keywords = ['debit', 'withdrawal', 'expense', 'cost', 'payment', 'spent', 'out']
         val = next((c for c in found_cols if any(k in c for k in debit_keywords)), None)
         if val:
            df.rename(columns={val: 'debit'}, inplace=True)

    # Clean up
    if 'debit' not in df.columns: df['debit'] = 0
    if 'credit' not in df.columns: df['credit'] = 0
    
    # Handle 'Amount' single column case (Negative = Debit, Positive = Credit)
    if 'amount' in df.columns and df['debit'].sum() == 0 and df['credit'].sum() == 0:
         df['credit'] = df['amount'].apply(lambda x: x if x > 0 else 0)
         df['debit'] = df['amount'].apply(lambda x: abs(x) if x < 0 else 0)

    # Ensure numeric
    for col in ['credit', 'debit']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    return df
