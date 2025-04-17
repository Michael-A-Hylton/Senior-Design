import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

df = pd.read_csv('C:\\Users\\bfire\\Desktop\\CSUSpring2025\\Senior_Design\\simulated_tax_data.csv')
print(df.info())
print(df.head())
df['filing_status'] = df['filing_status'].map({'single': 0, 'head': 1, 'joint': 2})

X = df[[
    'income', 'num_employees', 'facility_exp', 'referral_exp', 'fuel_exp', 'mileage',
    'research_exp', 'adv_energy_exp', 'energy_home_exp', 'deferred_gain',
    'basis_value', 'direct_wages', 'tips', 'hours_worked', 'home_office_sqft',
    'filing_status'
]]

# Multi-label outputs
y = df[[
    'childcare_credit', 'fuel_tax_credit', 'research_credit', 'clean_vehicle_credit',
    'advanced_energy_credit', 'energy_eff_home_credit', 'opp_zone_credit',
    'fica_tip_credit', 'mileage_deduction', 'home_office_deduction'
]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the multi-label model
base_model = RandomForestClassifier(n_estimators=100, random_state=42)
model = MultiOutputClassifier(base_model)

# Train the model
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=y.columns))

joblib.dump(model, 'models/wealthwise_multi_label_model.pkl')
