import pandas as pd
from typing import List, Dict, Any

# Step 1: Risk Identification
def load_risk_register(csv_path: str) -> pd.DataFrame:
    """Load the risk register CSV into a DataFrame."""
    df = pd.read_csv(csv_path)
    return df

def identify_risks(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Extract and return risks as dicts from the DataFrame."""
    risks = df.to_dict('records')
    return risks

# Step 2: Risk Analysis (Qualitative, Quantitative)
def qualitative_analysis(risk: Dict[str, Any]) -> str:
    """Perform qualitative analysis, return qualitative rating (stub)."""
    prob = risk.get('Probability_Rating', '')
    impact = risk.get('Impact_Rating', '')
    if prob == "High" and impact == "High":
        return "Critical"
    elif prob == "Medium" or impact == "High":
        return "Major"
    else:
        return "Minor"

def quantitative_analysis(risk: Dict[str, Any]) -> int:
    """Perform quantitative analysis, return a risk score (stub)."""
    # Example stub: use 'Risk_Score' if present, else simple calculation
    try:
        score = int(risk.get('Risk_Score', 0))
    except Exception:
        score = 0
    if score == 0:
        # Fallback calculation: assign numbers to ratings
        prob_map = {"High": 3, "Medium": 2, "Low": 1}
        impact_map = {"High": 3, "Medium": 2, "Low": 1}
        score = prob_map.get(risk.get('Probability_Rating', ''), 1) * impact_map.get(risk.get('Impact_Rating', ''), 1)
    return score

# Step 3: Plan Risk Responses
def recommend_response(risk: Dict[str, Any], qual_rating: str, quant_score: int) -> str:
    """Recommend a risk response based on analysis."""
    # Example stub logic
    if qual_rating == "Critical" or quant_score >= 9:
        return "Immediate mitigation required. Assign risk owner and escalate."
    elif qual_rating == "Major" or quant_score >= 6:
        return "Mitigation plan needed. Monitor closely."
    else:
        return "Standard monitoring and documentation."

# Step 4: Monitor & Control
def monitor_control(risk: Dict[str, Any], response: str) -> str:
    """Stub for monitoring and control actions."""
    # Example: suggest monitoring frequency based on response
    if "Immediate" in response:
        return "Weekly review required."
    elif "Mitigation plan" in response:
        return "Monthly review recommended."
    else:
        return "Quarterly review sufficient."

# Step 5: Documentation
def document_recommendation(risk: Dict[str, Any], qual_rating: str, quant_score: int, response: str, monitor: str) -> Dict[str, Any]:
    """Compile documentation for the risk and its recommendation."""
    return {
        "Risk_ID": risk.get("Risk_ID"),
        "Risk_Title": risk.get("Risk_Title"),
        "Qualitative_Rating": qual_rating,
        "Quantitative_Score": quant_score,
        "Recommended_Response": response,
        "Monitoring_Action": monitor,
        "Documented_By": "RMS Recommender System"
    }

# Main pipeline function
def process_risks(csv_path: str) -> List[Dict[str, Any]]:
    df = load_risk_register(csv_path)
    risks = identify_risks(df)
    recommendations = []
    for risk in risks:
        qual_rating = qualitative_analysis(risk)
        quant_score = quantitative_analysis(risk)
        response = recommend_response(risk, qual_rating, quant_score)
        monitor = monitor_control(risk, response)
        doc = document_recommendation(risk, qual_rating, quant_score, response, monitor)
        recommendations.append(doc)
    return recommendations

if __name__ == "__main__":
    # Example usage
    csv_path = "network_infrastructure_risk_register.csv"
    recommendations = process_risks(csv_path)
    for rec in recommendations[:5]:  # Print first 5 for brevity
        print(rec)
