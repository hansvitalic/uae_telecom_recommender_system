import csv
import os

CSV_FILE = "sample_network_infrastructure_risk_register.csv"

def read_risks(csv_file):
    risks = []
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            risks.append(row)
    return risks

def test_column_integrity(risks, expected_columns):
    for row in risks:
        assert set(row.keys()) == set(expected_columns), f"Column mismatch: {row.keys()}"

def test_row_population(risks):
    for i, row in enumerate(risks):
        for k, v in row.items():
            assert v != "", f"Empty value in row {i+1}, column '{k}'"

def test_duplicate_ids(risks):
    ids = [row['Risk_ID'] for row in risks]
    assert len(ids) == len(set(ids)), "Duplicate Risk_IDs found"

def test_extreme_scores(risks):
    for row in risks:
        score = int(row['Risk_Score'])
        assert 0 <= score <= 10 or score >= 11, f"Risk_Score out of expected range: {score}"

def recommend_actions_for_risk(risk_row):
    # Dummy logic; replace with your recommender function
    if risk_row['Impact_Rating'] == 'High' and risk_row['Probability_Rating'] == 'High':
        return "Immediate mitigation required"
    elif risk_row['Impact_Rating'] == 'Medium':
        return "Monitor and review quarterly"
    else:
        return "Standard review"

def test_recommender_logic(risks):
    for row in risks:
        action = recommend_actions_for_risk(row)
        assert action in [
            "Immediate mitigation required",
            "Monitor and review quarterly",
            "Standard review"
        ], f"Unexpected recommendation for Risk_ID={row['Risk_ID']}: {action}"

def main():
    assert os.path.exists(CSV_FILE), f"CSV file {CSV_FILE} not found"
    risks = read_risks(CSV_FILE)
    expected_columns = [
        'Risk_ID','Risk_Title','Risk_Description','Probability_Rating','Impact_Rating','Category','Sub_Category',
        'Sector','Stakeholder_Group','Project_Phase','Risk_Owner','Mitigation_Action','Response_Strategy','Risk_Score',
        'Last_Updated','Status','Documentation_Required','Detection_Method','Source','System','Asset','Threat','Control',
        'Control_Effectiveness','Residual_Risk','Review_Frequency','Cost_Impact','Time_Impact','Reputation_Impact',
        'Legal_Impact','Compliance_Impact','Financial_Impact','Operational_Impact','Safety_Impact','Environment_Impact',
        'Risk_Trend','Notes','Attachments','Approval_Status'
    ]
    test_column_integrity(risks, expected_columns)
    test_row_population(risks)
    test_duplicate_ids(risks)
    test_extreme_scores(risks)
    test_recommender_logic(risks)
    print("All tests passed!")

if __name__ == "__main__":
    main()