"""
Ollama AI Integration for Bank Customer Churn Analysis

Uses local LLMs via Ollama to:
1. Generate natural language explanations of churn predictions
2. Provide personalized retention recommendations
3. Analyze customer risk factors in plain English

Prerequisites:
  - Install Ollama from https://ollama.com
  - Pull a model: ollama pull llama3.2:1b  (lightweight, works on CPU)
  - Or: ollama pull mistral:7b  (more capable, needs more RAM)
"""

import json
import os
import requests
from typing import Optional, Dict, Any

# ─── Configuration ───────────────────────────────────────────────────────────
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:1b")
OLLAMA_TIMEOUT = int(os.environ.get("OLLAMA_TIMEOUT", "30"))


def is_ollama_available() -> bool:
    """Check if Ollama server is running and the model is available."""
    try:
        resp = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if resp.status_code == 200:
            models = resp.json().get("models", [])
            available_models = [m["name"] for m in models]
            # Check if our model (or any model) is available
            if OLLAMA_MODEL in available_models:
                return True
            # If the exact model isn't found but Ollama is running, still return True
            # (the generate call will pull it automatically if needed)
            return len(available_models) > 0
        return False
    except (requests.ConnectionError, requests.Timeout):
        return False


def generate_ollama_response(prompt: str, system_prompt: str = None) -> Optional[str]:
    """
    Send a prompt to Ollama and get the response.
    
    Args:
        prompt: The user prompt / question
        system_prompt: Optional system-level instruction
        
    Returns:
        Generated text response, or None if Ollama is unavailable
    """
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,  # Low temperature for more deterministic outputs
            "num_predict": 512,  # Max tokens to generate
        }
    }
    
    if system_prompt:
        payload["system"] = system_prompt
    
    try:
        resp = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json=payload,
            timeout=OLLAMA_TIMEOUT
        )
        if resp.status_code == 200:
            return resp.json().get("response", "").strip()
        return None
    except (requests.ConnectionError, requests.Timeout, json.JSONDecodeError):
        return None


def explain_prediction(
    customer_data: Dict[str, Any],
    prediction: int,
    probability: float,
    lang: str = "en"
) -> Dict[str, str]:
    """
    Use Ollama to generate a natural language explanation of a churn prediction.
    
    Args:
        customer_data: Dictionary of customer features
        prediction: 0 (retain) or 1 (churn)
        probability: Churn probability (0-100)
        lang: Language code (en/hi/te)
        
    Returns:
        Dictionary with 'explanation', 'recommendation', and 'risk_factors' keys
    """
    risk_level = "high" if prediction == 1 else "low"
    
    # Build a concise customer profile for the prompt
    profile = (
        f"Customer Profile:\n"
        f"- Credit Score: {customer_data.get('credit_score', 'N/A')}\n"
        f"- Geography: {customer_data.get('geography', 'N/A')}\n"
        f"- Gender: {customer_data.get('gender', 'N/A')}\n"
        f"- Age: {customer_data.get('age', 'N/A')}\n"
        f"- Tenure: {customer_data.get('tenure', 'N/A')} years\n"
        f"- Balance: ${customer_data.get('balance', 'N/A')}\n"
        f"- Products: {customer_data.get('num_products', 'N/A')}\n"
        f"- Has Credit Card: {'Yes' if customer_data.get('has_cr_card') else 'No'}\n"
        f"- Active Member: {'Yes' if customer_data.get('is_active_member') else 'No'}\n"
        f"- Estimated Salary: ${customer_data.get('estimated_salary', 'N/A')}\n"
        f"\n"
        f"ML Model Prediction: {'WILL CHURN' if prediction == 1 else 'WILL STAY'}\n"
        f"Churn Probability: {probability:.1f}%\n"
        f"Risk Level: {risk_level.upper()}"
    )
    
    system_prompt = (
        "You are a bank customer retention analyst AI. "
        "Analyze customer data and provide clear, actionable insights. "
        "Keep responses concise (2-3 sentences max per section). "
        "Be professional and data-driven."
    )
    
    # Generate explanation
    explanation_prompt = (
        f"{profile}\n\n"
        f"Based on this customer's data and the ML prediction, "
        f"explain in simple terms why this customer is at {'high' if prediction == 1 else 'low'} risk of churning. "
        f"Mention specific factors from their profile that contribute to this prediction."
    )
    
    # Generate recommendation
    recommendation_prompt = (
        f"{profile}\n\n"
        f"Suggest 2-3 specific, actionable retention strategies "
        f"that a bank relationship manager could use for this customer. "
        f"Tailor recommendations to their specific situation."
    )
    
    # Generate risk factors
    risk_prompt = (
        f"{profile}\n\n"
        f"List the top 3 risk factors for this customer in order of importance. "
        f"Format as a simple numbered list with brief explanations."
    )
    
    # Make parallel calls to Ollama
    explanation = generate_ollama_response(explanation_prompt, system_prompt)
    recommendation = generate_ollama_response(recommendation_prompt, system_prompt)
    risk_factors = generate_ollama_response(risk_prompt, system_prompt)
    
    return {
        "explanation": explanation or "AI explanation unavailable. Please ensure Ollama is running.",
        "recommendation": recommendation or "Recommendations unavailable.",
        "risk_factors": risk_factors or "Risk factor analysis unavailable.",
        "model_used": OLLAMA_MODEL,
        "ai_available": explanation is not None
    }


def analyze_dashboard_insights(dashboard_data: Dict[str, Any], lang: str = "en") -> Optional[str]:
    """
    Use Ollama to generate a high-level summary/insight from dashboard data.
    
    Args:
        dashboard_data: Dashboard analytics data
        lang: Language code
        
    Returns:
        Natural language summary, or None if unavailable
    """
    summary_data = {
        "total_customers": dashboard_data.get("total_customers"),
        "churn_rate": dashboard_data.get("churn_rate"),
        "active_members": dashboard_data.get("active_members"),
        "avg_age": dashboard_data.get("avg_age"),
        "avg_balance": dashboard_data.get("avg_balance"),
        "avg_credit_score": dashboard_data.get("avg_credit_score"),
        "churn_by_geo": dashboard_data.get("churn_by_geo", {}),
    }
    
    prompt = (
        f"Here is the bank customer churn dashboard data:\n"
        f"{json.dumps(summary_data, indent=2)}\n\n"
        f"Provide a brief 3-4 sentence executive summary of the key insights "
        f"and trends visible in this data. Focus on actionable takeaways "
        f"for the bank's retention team."
    )
    
    system_prompt = (
        "You are a data analyst providing executive summaries. "
        "Be concise, insightful, and focus on actionable business intelligence."
    )
    
    return generate_ollama_response(prompt, system_prompt)