from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, LoginManager, UserMixin, login_user, logout_user, current_user
import sqlite3
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

app = Flask(__name__, template_folder=("."))#Pull the html files from current directory
import waitress
@app.route('/')
def index():
    return render_template('frontEnd.html') #defualt webpage

@app.route('/submitAllFields')
def submitAllFields():
    gross_Rev = request.form['grossRev']
    net_Income=request.form['netIncome']
    taxable_Income = request.form['Taxable_Income']
    operating_Expenses = request.form['operatingExpenses']
    user_input = {
        "Gross_Revenue": gross_Rev,
        "Net_Income": net_Income,
        "Taxable_Income": taxable_Income,
        "Operating_Expenses": operating_Expenses
    }
    '''
    
    business_Name=request.form['businessName']
    entity_Type=request.form['entityType']
    location=request.form['location']
    years_in_Business=request.form['yearsInBusiness']
    industry=request.form['industry']
    #income_Growth_Rate=request.form['incomeGrowthRate']
    deprec_and_Amort=request.form['DeprecAmort']
    interest_Expenses=request.form['interestExpenses']
    rnd_Expenses=request.form['r&dExpenses']
    home_Office_Deduction=request.form['homeOfficeDeduction']
    number_of_Employees=request.form['numberofEmployees']
    payroll_Expenses=request.form['payrollExpenses']
    retirement_Plan_Contributions=request.form['retirementPlanContributions']
    healthcare_Expenses=request.form['healthcareExpenses']
    sales_Tax_Obligations=request.form['salesTaxObligations']
    #inventory_Method=request.form['inventoryMethod']
    cost_of_Goods_Sold=request.form['costOfGoodsSold']
    # fixed_Assets=request.form['fixedAssets']
    capital_Expenditures=request.form['capitalExpenditures']
    property_Ownership_Status=request.form['propertyOwnershipStatus']
    vehicle_Use=request.form['vehicleUse']
    rnD_Credits=request.form['rndCredits']
    energy_Efficiency_Credits=request.form['energyEfficiencyCredits']
    work_Opportunity_Tax_Credit=request.form['workOpportunityTaxCredit']
    employee_Retention_Credits=request.form['employeeRetentionCredits']
    outstanding_Debt=request.form['outstandingDebt']
    interest_Payments=request.form['interestPayments']
    loan_Type=request.form['loan_Type']
    business_Investments=request.form['businessInvestments']
    retirement_Contributions=request.form['retirementContributions']
    previous_Tax_Liabilities=request.form['previousTaxLiabilities']
    tax_Filing_Method=request.form['taxFilingMethod']
    carryforwards_and_Carrybacks=request.form['carryforwardsAndCarrybacks']
    Current_Tax_Strategy=request.form['CurrentTaxStrategy']
    revenue_Streams=request.form['revenue_Streams']
    domestic_vs_Foreign_Income=request.form['domesticVsForeignIncome']
    major_Asset_Sales=request.form['majorAssetSales']
    capital_Gains_and_Losses=request.form['capitalGainsAndLosses']
    
    return render_template('frontEnd.html')
    '''
    return(user_input)
def loadData():
    dataFP = "C:\\Users\\bfire\\OneDrive\\Desktop\\CSUSpring2025\\Senior_Design\\Updated_Business_Tax_Strategy_Data - Updated_Business_Tax_Strategy_Data.csv"
    df = pd.read_csv(dataFP)
    df.info(), df.head()
    return(df)


def preprocess_data(df, numeric_features):
    """Scale numeric features for similarity calculations."""
    scaler = StandardScaler()
    df_scaled = df.copy()
    df_scaled[numeric_features] = scaler.fit_transform(df[numeric_features])
    return df_scaled, scaler


def find_similar_businesses(user_input, df, numeric_features, scaler, top_n=5):
    """Find similar businesses based on numerical features."""
    user_df = pd.DataFrame([user_input])
    user_df[numeric_features] = scaler.transform(user_df[numeric_features])

    similarities = cosine_similarity(user_df[numeric_features], df[numeric_features])
    df["similarity_score"] = similarities[0]

    return df.nlargest(top_n, "similarity_score")


def generate_suggestions(similar_businesses):
    """Generate tax optimization suggestions based on similar businesses."""
    suggestions = []

    # Example heuristic rules based on similar businesses
    avg_tax_liability = similar_businesses["Previous_Tax_Liabilities"].mean()
    avg_r_d_credit = similar_businesses["R&D_Credits"].mean()
    avg_deductions = similar_businesses[["Depreciation_and_Amortization", "Home_Office_Deduction"]].sum(axis=1).mean()

    if avg_tax_liability > 50000:
        suggestions.append("Consider restructuring as an LLC to reduce liability.")
    elif avg_tax_liability > 100000:
        suggestions.append("Consider restructuring as a C-Corp to reduce tax rate.")
    if avg_r_d_credit > 5000:
        suggestions.append("Consider  restructuring as an LLC to reduce self-employment taxes.")

    if avg_deductions < 10000:
        suggestions.append("You might be missing key deductions such as home office or depreciation.")

    return suggestions


# Example Usage
df = loadData()
numeric_features = ["Gross_Revenue", "Net_Income", "Taxable_Income", "Operating_Expenses",
                    "Depreciation_and_Amortization"]
df_scaled, scaler = preprocess_data(df, numeric_features)

user_input=submitAllFields
similar_businesses = find_similar_businesses(user_input, df_scaled, numeric_features, scaler)
suggestions = generate_suggestions(similar_businesses)
print("Tax Optimization Suggestions:")
for s in suggestions:
    print(f"- {s}")
def extractVectors(data, customer_keys):
    vectors = data[data["CustomerKey"].isin(customer_keys)].drop(columns=["CustomerKey"])
    return vectors.values  # Convert to NumPy array


waitress.serve(app, host='0.0.0.0', port=5004)