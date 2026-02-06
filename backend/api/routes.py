from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.parser import parse_financial_file
from services.financial_metrics import calculate_financial_health
from services.llm import generate_insights
import pandas as pd
import json

router = APIRouter()

@router.post("/analyze-file")
async def analyze_file(
    file: UploadFile = File(...),
    business_type: str = Form("Retail"),
    language: str = Form("English")
):
    # 1. Parse
    try:
        df = await parse_financial_file(file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # 2. Analyze Metrics
    try:
        metrics = calculate_financial_health(df)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    # 3. Get LLM Insights
    metrics['business_type'] = business_type
    insights = generate_insights(metrics, language)
    
    return {
        "metrics": metrics,
        "insights": insights
    }

@router.get("/sample-data")
def get_sample_data():
    return {
        "download_url": "/static/sample_statement.csv" 
    }
