import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_insights(financial_data: dict, language: str = "English"):
    print(f"DEBUG: API Key present: {bool(GEMINI_API_KEY)}")
    if not GEMINI_API_KEY:
        print("DEBUG: No API Key found, using mock.")
        return mock_insights(language, financial_data)
        
    prompt = f"""
    You are a financial advisor for a Small/Medium Enterprise (SME).
    Analyze the following financial summary:
    - Business Type: {financial_data.get('business_type', 'General')}
    - Score: {financial_data['score']}/100
    - Total Revenue: {financial_data['total_revenue']}
    - Total Expenses: {financial_data['total_expenses']}
    - Debt Obligations: {financial_data.get('debt_obligations', 0)}
    - Tax Status: {financial_data.get('tax_compliance', 'N/A')}
    - Risks: {', '.join(financial_data['risks'])}
    
    Provide a professional financial assessment in {language}.
    Structure your response exactly as follows (keep formatting clean):
    
    **Financial Health:** [Explain the score and overall situation in 2-3 sentences]
    
    **Key Observations:**
    *   [Observation 1]
    *   [Observation 2]
    
    **Actionable Tips:**
    1. [Tip 1]
    2. [Tip 2]
    3. [Tip 3]
    
    **Working Capital Recommendation:** [Specific advice on working capital]
    
    Note: Keep the tone helpful, professional, and encouraging.
    """
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        print("DEBUG: Gemini response received.")
        return response.text
    except Exception as e:
        print(f"DEBUG: LLM Error: {e}")
        import traceback
        traceback.print_exc()
        return mock_insights(language, financial_data)

def mock_insights(language="English", data=None):
    if not data:
        data = {}

    score = data.get('score', 50)
    revenue = data.get('total_revenue', 0)
    expenses = data.get('total_expenses', 0)
    debt = data.get('debt_obligations', 0)
    business_type = data.get('business_type', 'Retail')
    
    # Logic for Health Status
    health_status = "stable"
    if score > 75: health_status = "excellent"
    elif score < 40: health_status = "critical"
    
    # Logic for Tips based on Business Type
    tips = []
    
    if business_type == 'Retail':
        tips = [
            "Optimize inventory turnover to reduce holding costs.",
            "Analyze peak sales hours to staff efficiently.",
            "Negotiate bulk discounts with top suppliers."
        ]
    elif business_type == 'Manufacturing':
        tips = [
            "Review raw material sourcing contracts for better rates.",
            "Implement preventative maintenance to reduce downtime costs.",
            "Optimize energy consumption during peak production hours."
        ]
    elif business_type == 'Agri':
        tips = [
            "Invest in better storage to reduce post-harvest losses.",
            "Review crop insurance options for better risk coverage.",
            "Explore direct-to-market channels to increase margins."
        ]
    elif business_type == 'Logistics':
        tips = [
            "Optimize route planning to reduce fuel consumption.",
            "Implement regular vehicle maintenance to avoid costly repairs.",
            "Review driver efficiency and idle times."
        ]
    elif business_type == 'Ecommerce':
        tips = [
            "Analyze customer acquisition costs (CAC) vs lifetime value (LTV).",
            "Optimize shipping partners to reduce logistics costs.",
            "Focus on reducing cart abandonment rates."
        ]
    else: # General/Services
         tips = [
            "Review recurring software subscriptions.",
            "Negotiate better payment terms with suppliers.",
            "Focus on collecting receivables faster."
        ]

    # Dynamic Adjustments based on Financials
    if expenses > revenue:
        tips.insert(0, "⚠️ IMMEDIATE ACTION: Expenses exceed Revenue. Cut discretionary spending.")
        health_status = "losing money"
    
    if debt > (revenue * 0.3):
        tips.append("High Debt Alert: Focus on clearing high-interest loans first.")
        
    tips = tips[:3] # Keep top 3

    # Language Generation
    if language == "Hindi":
        status_map = {
            "stable": "स्थिर है",
            "excellent": "उत्कृष्ट है",
            "critical": "नाज़ुक है",
            "losing money": "घाटे में है"
        }
        
        hindi_tips = [
            "1. अनावश्यक खर्चों की तुरंत समीक्षा करें।",
            "2. अपने आपूर्तिकर्ताओं (vendors) के साथ बेहतर शर्तों पर बात करें।",
            "3. नकदी प्रवाह (Cash Flow) को सुधारने पर ध्यान दें।"
        ]
        
        # Simple override for specific business types in Hindi (basic translation)
        if business_type == 'Agri':
            hindi_tips = [
                "1. फसल बीमा विकल्पों की समीक्षा करें।",
                "2. बेहतर भंडारण (Storage) में निवेश करें।",
                "3. बिचौलियों को कम करके सीधे बाजार में बेचें।"
            ]
        elif business_type == 'Retail':
             hindi_tips = [
                "1. इन्वेंट्री (Inventory) को जल्दी बेचने पर ध्यान दें।",
                "2. पीक सेल्स समय के अनुसार स्टाफिंग करें।",
                "3. थोक खरीद पर डिस्काउंट मांगें।"
            ]

        if expenses > revenue:
             hindi_tips.insert(0, "⚠️ चेतावनी: आपके खर्च आपकी आय से अधिक हैं।")

        return f"""
        **वित्तीय स्वास्थ्य:** वर्तमान डेटा के आधार पर, आपकी वित्तीय स्थिति **{status_map.get(health_status, 'स्थिर')}**।
        
        **प्रमुख सुझाव ({business_type}):**
        {chr(10).join(hindi_tips[:3])}
        
        **कार्यशील पूंजी सलाह:**
        आपातकालीन निधि (Emergency Fund) बनाए रखें और कम से कम 3 महीने के खर्चों के बराबर नकदी सुरक्षित रखें।
        """

    else:
        return f"""
        **Financial Health:** Based on the analysis, your business health is **{health_status}**. {f"Your annual revenue is {revenue:,.0f}." if revenue > 0 else ""}
        
        **Actionable Tips for {business_type}:**
        1. {tips[0]}
        2. {tips[1]}
        3. {tips[2]}
        
        **Working Capital Recommendation:**
        Based on your score of {score}/100, we recommend maintaining a cash buffer of at least 15% of your monthly turnover. {"Consider a short-term working capital loan." if score > 60 else "Focus on improving cash flow before taking new loans."}
        """
