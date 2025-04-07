from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Retrieve form values
    filing_status = request.form.get('filing-status')
    income = float(request.form.get('income', 0))

    # Childcare Credit
    childcare_credit = 0
    if 'childcare-credit-toggle' in request.form:
        facility_exp = float(request.form.get('facility-exp', 0))
        referral_exp = float(request.form.get('referral-exp', 0))
        childcare_credit = (0.25 * facility_exp) + (0.10 * referral_exp)
        childcare_credit = min(childcare_credit, 150000)

    # Opportunity Zone Credit
    opp_zone_credit = 0
    if 'opp-zone-toggle' in request.form:
        deferred_gain = float(request.form.get('deferred-gain', 0))
        fmv = float(request.form.get('fair-market-value', 0))
        basis = float(request.form.get('basis-value', 0))
        reportable_gain = max(0, min(deferred_gain, fmv) - basis)
        opp_zone_credit = reportable_gain

    # Fuel Tax Credit
    fuel_tax_credit = 0
    if 'fuel-tax-toggle' in request.form:
        fuel_expenses = float(request.form.get('fuel-exp', 0))
        fuel_tax_credit = fuel_expenses

    # Clean Vehicle Credit
    clean_vehicle_credit = 0
    if 'clean-vehicle-credit' in request.form:
        # Clean vehicle credit only applies if income is below a certain threshold
        limit = 150000
        if filing_status == 'head':
            limit = 225000
        elif filing_status == 'joint':
            limit = 300000
        if income <= limit:
            clean_vehicle_credit = 7500
    if 'childcare-credit-toggle' in request.form:
        childcare_establishment_exp = float(request.form.get('facility-exp', 0))
        childcare_operating_exp = float(request.form.get('referral-exp', 0))
        childcare_credit = (0.25 * childcare_establishment_exp) + (0.10 * childcare_operating_exp)
        childcare_credit = min(childcare_credit, 150000)  # Limit on this credit

        # Energy Efficient Home Credit
    energy_eff_home_credit = 0
    if 'energy-eff-home-toggle' in request.form:
        energy_eff_home_credit = float(request.form.get('energy-eff-home-exp', 0))  # Maximum is $5,000

    # Advanced Energy Project Credit
    advanced_energy_project_credit = 0
    if 'advanced-energy-project-toggle' in request.form:
        advanced_energy_project_credit = float(
            request.form.get('advanced-energy-project-exp', 0))  # Example calculation

    # Work Opportunity Tax Credit (WOTC)
    wotc_credit = 0
    if 'wotc-toggle' in request.form:
        # This credit is often based on the number of qualifying employees, assumed max value here
        wotc_credit = 2400  # Maximum WOTC value for some groups, adjust for actual calculations.

    # Research Credit
    research_credit = 0
    if 'research-credit-toggle' in request.form:
        research_expenses = float(request.form.get('research-expenses', 0))
        research_credit = 0.2 * research_expenses  # 20% of research expenses, simplified

    # Other Credits (already present)
    clean_vehicle_credit = 0
    if 'clean-vehicle-credit' in request.form:
        limit = 150000
        if filing_status == 'head':
            limit = 225000
        elif filing_status == 'joint':
            limit = 300000
        if income <= limit:
            clean_vehicle_credit = 7500  # Maximum credit for clean vehicle


    # Other credits
    other_credits = 0
    credit_names = ['credit', 'credit-2', 'credit-3', 'credit-4', 'credit-5', 'credit-6', 'credit-7', 'credit-8']
    for credit in credit_names:
        if credit in request.form:
            other_credits += float(request.form.get(credit, 0))

    # Deduction values
    deductions = 0
    if 'deductions' in request.form:
        deductions = sum([float(request.form.get(f'deduction-{i}', 0)) for i in range(1, 5)])

    # Calculate the total savings
    total_deductions=0

    # Adding all credits
    total_credits = (
            childcare_credit +
            energy_eff_home_credit +
            advanced_energy_project_credit +
            wotc_credit +
            research_credit +
            clean_vehicle_credit
            + opp_zone_credit
            + fuel_tax_credit
            + clean_vehicle_credit
            + other_credits
    )
    estimated_savings = total_deductions+total_credits
    # Return the results
    return render_template('results.html', income=income, total_deductions=total_deductions, savings=estimated_savings)

if __name__ == '__main__':
    app.run(debug=True)