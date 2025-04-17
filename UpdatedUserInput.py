# === CONFIGURATION ===
DATASET_PATH = 'simulated_tax_data.csv'
MODEL_PATH = 'models/wealthwise_multi_label_model.pkl'

# === IMPORTS ===
from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import os
import joblib

# === CONSTANTS ===
LABELS = [
    'childcare_credit', 'fuel_tax_credit', 'research_credit', 'clean_vehicle_credit',
    'advanced_energy_credit', 'energy_eff_home_credit', 'opp_zone_credit',
    'fica_tip_credit', 'mileage_deduction', 'home_office_deduction'
]
FILING_STATUS_ENCODING = {'single': 0, 'head': 1, 'joint': 2}

# === INITIALIZE FLASK APP ===
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('UpdatedIndex.html')

def encode_filing_status(status):
    return FILING_STATUS_ENCODING.get(status, 0)

def safe_float(form, name, default=0.0):
    try:
        return float(form.get(name, default) or default)
    except (ValueError, TypeError):
        return default

def get_credit_recommendations(form):
    try:
        features = [
            safe_float(form, 'income'),
            safe_float(form, 'num-employees'),
            safe_float(form, 'facility-exp'),
            safe_float(form, 'referral-exp'),
            safe_float(form, 'fuel-exp'),
            safe_float(form, 'business-miles'),
            safe_float(form, 'research-expenses'),
            safe_float(form, 'advanced-energy-project-exp'),
            safe_float(form, 'energy-eff-home-exp'),
            safe_float(form, 'deferred-gain'),
            safe_float(form, 'basis-value'),
            safe_float(form, 'direct-wages'),
            safe_float(form, 'total-tips'),
            safe_float(form, 'hours-worked'),
            safe_float(form, 'home-office-sqft'),
            encode_filing_status(form.get('filing-status', 'single'))
        ]
    except ValueError:
        return []

    columns = [
        'income', 'num_employees', 'facility_exp', 'referral_exp', 'fuel_exp', 'mileage',
        'research_exp', 'adv_energy_exp', 'energy_home_exp', 'deferred_gain',
        'basis_value', 'direct_wages', 'tips', 'hours_worked', 'home_office_sqft',
        'filing_status'
    ]

    input_df = pd.DataFrame([features], columns=columns)
    model = joblib.load(MODEL_PATH)
    prediction = model.predict(input_df)[0]

    return [label for label, p in zip(LABELS, prediction) if p == 1]

def save_user_data(form):
    record = {
        'income': safe_float(form, 'income'),
        'num_employees': safe_float(form, 'num-employees'),
        'facility_exp': safe_float(form, 'facility-exp'),
        'referral_exp': safe_float(form, 'referral-exp'),
        'fuel_exp': safe_float(form, 'fuel-exp'),
        'mileage': safe_float(form, 'business-miles'),
        'research_exp': safe_float(form, 'research-expenses'),
        'adv_energy_exp': safe_float(form, 'advanced-energy-project-exp'),
        'energy_home_exp': safe_float(form, 'energy-eff-home-exp'),
        'deferred_gain': safe_float(form, 'deferred-gain'),
        'basis_value': safe_float(form, 'basis-value'),
        'direct_wages': safe_float(form, 'direct-wages'),
        'tips': safe_float(form, 'total-tips'),
        'hours_worked': safe_float(form, 'hours-worked'),
        'home_office_sqft': safe_float(form, 'home-office-sqft'),
        'filing_status': form.get('filing-status', 'single')
    }

    labels = {label: int(f"{label.replace('_', '-')}-toggle" in form) for label in LABELS}
    df = pd.DataFrame([{**record, **labels}])
    header = not os.path.exists(DATASET_PATH)
    df.to_csv(DATASET_PATH, mode='a', header=header, index=False)

@app.route('/calculate', methods=['POST'])
def calculate():
    form = request.form
    income = safe_float(form, 'income')
    filing_status = form.get('filing-status')

    # === CREDIT CALCULATIONS ===
    childcare_credit = min((0.25 * safe_float(form, 'facility-exp') + 0.10 * safe_float(form, 'referral-exp')), 150000)
    opp_zone_credit = max(0, min(safe_float(form, 'deferred-gain'), safe_float(form, 'fair-market-value')) - safe_float(form, 'basis-value'))
    fuel_tax_credit = safe_float(form, 'fuel-exp')
    research_credit = 0.2 * safe_float(form, 'research-expenses')
    energy_eff_home_credit = safe_float(form, 'energy-eff-home-exp')
    advanced_energy_project_credit = 0.3 * safe_float(form, 'qualified-investment')
    fica_tip_credit = round(max(0, safe_float(form, 'total-tips') - max(0, 5.15 * safe_float(form, 'hours-worked') - safe_float(form, 'direct-wages'))) * 0.0765, 2)
    clean_vehicle_credit = 7500 if income <= (150000 if filing_status == 'single' else 225000 if filing_status == 'head' else 300000) else 0
    wotc_credit = 2400 if 'wotc-toggle' in form else 0

    try:
        num_employees = int(safe_float(form, 'num-employees'))
        num_nhces = int(safe_float(form, 'num-nhces'))
        startup_costs = safe_float(form, 'startup-costs')
        percent = 1.0 if num_employees <= 50 else 0.5 if num_employees <= 100 else 0.0
        base = startup_costs * percent
        limit = max(500, min(5000, 250 * num_nhces))
        retirement_startup_credit = min(base, limit)
    except: retirement_startup_credit = 0

    # === DEDUCTIONS ===
    sqft = safe_float(form, 'building-sqft')
    savings_pct = safe_float(form, 'energy-savings-percent')
    energy_efficient_building_deduction = round(sqft * min(1.0, 0.5 + 0.02 * max(0, savings_pct - 25)), 2) if 25 <= savings_pct <= 50 else 0

    interest_income = safe_float(form, 'business-interest-income')
    ati = safe_float(form, 'adjusted-taxable-income')
    floor_interest = safe_float(form, 'floor-plan-interest')
    business_interest_deduction = round(interest_income + 0.3 * ati + floor_interest, 2)

    mileage_deduction = round(safe_float(form, 'business-miles') * 0.70, 2)
    home_office_deduction = round(min(safe_float(form, 'home-office-sqft'), 300) * 5, 2)

    total_deductions = sum([
        energy_efficient_building_deduction,
        business_interest_deduction,
        mileage_deduction,
        home_office_deduction
    ])

    total_credits = sum([
        childcare_credit,
        energy_eff_home_credit,
        advanced_energy_project_credit,
        wotc_credit,
        research_credit,
        clean_vehicle_credit,
        retirement_startup_credit,
        fica_tip_credit,
        opp_zone_credit,
        fuel_tax_credit
    ])

    estimated_savings = total_deductions + total_credits
    recommended_credits = get_credit_recommendations(form)
    save_user_data(form)

    return render_template(
        'results.html',
        income=income,
        total_deductions=total_deductions,
        savings=estimated_savings,
        recommended_credits=recommended_credits
    )

if __name__ == '__main__':
    app.run(debug=True)
