import pandas as pd
import numpy as np

def calculate_monthly_metrics(df: pd.DataFrame):
    # Ensure Date is datetime
    try:
        df['date'] = pd.to_datetime(df['date'], dayfirst=True) # Assuming India format often
    except:
        # Fallback
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
    df = df.dropna(subset=['date'])
    
    # Fill NaN
    df['credit'] = df['credit'].fillna(0)
    df['debit'] = df['debit'].fillna(0)
    
    # Group by Month
    monthly = df.set_index('date').resample('ME').agg({
        'credit': 'sum',
        'debit': 'sum'
    }).reset_index()
    
    monthly['net_cash_flow'] = monthly['credit'] - monthly['debit']
    
    return monthly

def calculate_financial_health(df: pd.DataFrame):
    monthly_data = calculate_monthly_metrics(df)
    
    total_revenue = monthly_data['credit'].sum()
    total_expenses = monthly_data['debit'].sum()
    avg_monthly_revenue = monthly_data['credit'].mean()
    avg_monthly_burn = monthly_data['debit'].mean()
    
    # Risk Assessment
    risks = []
    
    # 1. Negative Cash Flow
    if total_expenses > total_revenue:
        risks.append("Burning more cash than earning (Negative Cash Flow)")
        
    # 2. Revenue Volatility (Std Dev / Mean)
    if avg_monthly_revenue > 0:
        cv = monthly_data['credit'].std() / avg_monthly_revenue
        if cv > 0.5:
            risks.append("High Revenue Volatility")
    
    
    # 3. Debt & EMI Obligations
    debt_keywords = ['emi', 'loan', 'interest', 'finance']
    debt_payments = df[df['description'].str.contains('|'.join(debt_keywords), case=False, na=False)]['debit'].sum()
    
    # 4. Tax Compliance
    tax_keywords = ['gst', 'tax', 'tds', 'duty']
    tax_payments = df[df['description'].str.contains('|'.join(tax_keywords), case=False, na=False)]['debit'].sum()
    tax_compliance_status = "Unclear"
    if tax_payments > 0:
        tax_compliance_status = "Tax Payments Detected"
    else:
        risks.append("No tax payments detected in this period")

    # Health Score (0-100)
    score = 50 # Base
    if total_revenue > total_expenses: score += 20
    if monthly_data['net_cash_flow'].iloc[-1] > 0: score += 10 # Last month positive
    
    # Debt Ratio Check (Mock: Debt Service Coverage Ratio approximation)
    if total_revenue > 0:
        debt_ratio = debt_payments / total_revenue
        if debt_ratio > 0.4:
            risks.append("High Debt Repayment Burden (>40% of revenue)")
            score -= 10
    
    # Deduct per risk
    score -= (len(risks) * 10)
    score = max(0, min(100, score))
    
    readiness = "Low"
    if score > 75: readiness = "High"
    elif score > 50: readiness = "Medium"
    
    # Convert monthly trend to simple types for JSON
    monthly_data['date'] = monthly_data['date'].dt.strftime('%Y-%m-%d')
    return {
        "score": int(score),
        "readiness": readiness,
        "total_revenue": float(total_revenue),
        "total_expenses": float(total_expenses),
        "net_cash_flow": float(total_revenue - total_expenses),
        "debt_obligations": float(debt_payments),
        "tax_compliance": tax_compliance_status,
        "risks": risks,
        "monthly_trend": monthly_data.to_dict(orient='records')
    }
