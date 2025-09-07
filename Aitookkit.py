# AI_QE_Toolkit.ipynb
# Micro AI tools for Quality Engineering CoE
# 1. Pharmacy Rule Drift Checker
# 2. Claim Adjudication Validator
# With Visual Dashboard

import pandas as pd
from difflib import SequenceMatcher
import matplotlib.pyplot as plt

# -------------------------------
# 1. Load sample data from Kaggle
# -------------------------------
# Make sure to download Kaggle datasets before running:
# !kaggle datasets download -d hiivus/pharmaceutical-drug-spending
# !unzip pharmaceutical-drug-spending.zip
# !kaggle datasets download -d cms/medicare-claims
# !unzip medicare-claims.zip

try:
    pharmacy_df = pd.read_csv("pharmaceutical_drug_spending.csv")
    claims_df = pd.read_csv("medicare_claims.csv")
    print("✅ Data Loaded: Pharmacy rows =", len(pharmacy_df), ", Claims rows =", len(claims_df))
except Exception as e:
    print("⚠️ Could not load Kaggle data, using fallback samples:", e)
    pharmacy_df = pd.DataFrame()
    claims_df = pd.DataFrame()


# -------------------------------
# 2. Pharmacy Rule Drift Checker
# -------------------------------
def pharmacy_rule_drift():
    print("\n🔍 Pharmacy Rule Drift Checker")

    # Simulated legacy vs new formulary/pricing rules
    legacy_rules = pd.DataFrame({
        "Drug": ["Atorvastatin", "Metformin", "Lisinopril"],
        "RuleText": [
            "Requires prior authorization if quantity > 30",
            "Step therapy required if generic available",
            "Max allowed 90 units per 90 days"
        ]
    })

    new_rules = pd.DataFrame({
        "Drug": ["Atorvastatin", "Metformin", "Lisinopril"],
        "RuleText": [
            "Requires prior authorization if quantity > 60",
            "No step therapy requirement",
            "Max allowed 90 units per 30 days"
        ]
    })

    def rule_similarity(rule1, rule2):
        return SequenceMatcher(None, rule1, rule2).ratio()

    results = []
    for _, row in legacy_rules.iterrows():
        new_rule = new_rules.loc[new_rules.Drug == row.Drug, "RuleText"].values[0]
        similarity = rule_similarity(row.RuleText, new_rule)
        results.append({
            "Drug": row.Drug,
            "LegacyRule": row.RuleText,
            "NewRule": new_rule,
            "Similarity": round(similarity, 2),
            "Status": "Changed" if similarity < 0.9 else "Same"
        })

    df = pd.DataFrame(results)

    # Visual dashboard
    plt.figure(figsize=(6,4))
    plt.bar(df["Drug"], df["Similarity"], color=["red" if s=="Changed" else "green" for s in df["Status"]])
    plt.ylim(0,1)
    plt.title("Pharmacy Rule Drift - Similarity Scores")
    plt.ylabel("Similarity (0-1)")
    for idx, val in enumerate(df["Similarity"]):
        plt.text(idx, val+0.02, str(val), ha='center')
    plt.show()

    return df


# -------------------------------
# 3. Claim Adjudication Validator
# -------------------------------
def claim_adjudication_validator():
    print("\n💰 Claim Adjudication Validator")

    if claims_df.empty:
        # fallback if Kaggle data missing
        sample_claims = pd.DataFrame({
            "ClaimID": [101, 102, 103],
            "BilledAmount": [500, 1200, 300],
            "PlanDeductible": [200, 500, 100],
            "PlanCopay": [50, 100, 25],
            "PlanOOPMax": [1000, 2000, 500]
        })
    else:
        sample_claims = claims_df.head(5).copy()
        sample_claims["PlanDeductible"] = [200, 500, 100, 300, 400]
        sample_claims["PlanCopay"] = [50, 100, 25, 75, 60]
        sample_claims["PlanOOPMax"] = [1000, 2000, 500, 1500, 1200]
        sample_claims["BilledAmount"] = sample_claims["Provider_Payment_Amount"].fillna(500)

    def adjudicate_claim(billed, deductible, copay, oopmax):
        covered = max(0, billed - deductible)
        member_pays = copay + deductible
        member_pays = min(member_pays, oopmax)
        plan_pays = billed - member_pays
        return member_pays, plan_pays

    results = []
    for _, row in sample_claims.iterrows():
        member, plan = adjudicate_claim(row.BilledAmount,
                                        row.PlanDeductible,
                                        row.PlanCopay,
                                        row.PlanOOPMax)
        results.append({
            "ClaimID": row.get("Claim_ID", row.name),
            "Billed": row.BilledAmount,
            "ExpectedMemberPay": member,
            "ExpectedPlanPay": plan
        })

    df = pd.DataFrame(results)

    # Visual dashboard
    df.set_index("ClaimID")[["Billed", "ExpectedMemberPay", "ExpectedPlanPay"]].plot(
        kind="bar", figsize=(8,5))
    plt.title("Claim Adjudication Breakdown")
    plt.ylabel("Amount ($)")
    plt.xticks(rotation=0)
    plt.show()

    return df


# -------------------------------
# 4. Simple Menu
# -------------------------------
def run_toolkit():
    print("\n==== AI QE Toolkit ====")
    print("1. Pharmacy Rule Drift Checker")
    print("2. Claim Adjudication Validator")

    choice = input("Select an option (1/2): ")
    if choice == "1":
        return pharmacy_rule_drift()
    elif choice == "2":
        return claim_adjudication_validator()
    else:
        return "❌ Invalid choice"

# Run toolkit
output = run_toolkit()
output
