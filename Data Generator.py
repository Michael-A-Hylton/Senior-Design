import pandas as pd
import numpy as np

# Define the number of businesses to generate
num_samples = 500

# Generate synthetic data
np.random.seed(42)

data = {
    "Business_ID": np.arange(10000, 10000 + num_samples),
    "Industry": np.random.choice(["Tech", "Retail", "Manufacturing", "Healthcare", "Finance"], num_samples),
    "Business_Structure": np.random.choice(["LLC", "S-Corp", "C-Corp", "Sole Proprietorship"], num_samples),
    "Revenue_Streams": np.random.choice(["Software Sales", "Consulting", "E-commerce", "Subscription"], num_samples),
    "Property_Ownership_vs_Leasing": np.random.choice(["Owning", "Leasing"], num_samples),
    "Current_Tax_Strategy": np.random.choice(["Conservative", "Aggressive", "Balanced"], num_samples),
    "Years_in_Business": np.random.randint(1, 30, num_samples),
    "Previous_Tax_Liabilities": np.random.randint(5000, 50000, num_samples),
    "Gross_Revenue": np.random.randint(100000, 10000000, num_samples),
    "Net_Income": np.random.randint(50000, 5000000, num_samples),
    "Taxable_Income": np.random.randint(40000, 4500000, num_samples),
    "Income_Growth_Rate": np.random.uniform(-0.2, 0.3, num_samples),
    "Operating_Expenses": np.random.randint(20000, 2000000, num_samples),
    "Payroll_Expenses": np.random.randint(10000, 5000000, num_samples),
    "Retirement_Plan_Contributions": np.random.randint(2000, 50000, num_samples),
    "Healthcare_Expenses": np.random.randint(5000, 100000, num_samples),
    "Depreciation_and_Amortization": np.random.randint(1000, 100000, num_samples),
    "Interest_Expenses": np.random.randint(1000, 50000, num_samples),
    "R&D_Expenses": np.random.randint(0, 500000, num_samples),
    "R&D_Credits": np.random.randint(0, 50000, num_samples),
    "Energy_Efficiency_Credits": np.random.randint(0, 10000, num_samples),
    "Work_Opportunity_Tax_Credit (WOTC)": np.random.randint(0, 20000, num_samples),
    "Employee_Retention_Credits (ERC)": np.random.randint(0, 30000, num_samples),
    "Carryforwards_and_Carryback": np.random.randint(0, 50000, num_samples),
    "Home_Office_Deduction": np.random.randint(0, 5000, num_samples),
    "Fixed_Assets": np.random.randint(10000, 500000, num_samples),
    "Capital_Expenditures": np.random.randint(5000, 100000, num_samples),
    "Vehicle_Use_for_Business": np.random.randint(1000, 50000, num_samples),
    "Major_Asset_Sales": np.random.randint(0, 100000, num_samples),
    "Capital_Gains_and_Losses": np.random.randint(-50000, 100000, num_samples),
    "Outstanding_Debt": np.random.randint(10000, 1000000, num_samples),
    "Interest_Payments": np.random.randint(500, 50000, num_samples),
    "Loan_Type": np.random.choice(["Short-term", "Long-term", "Line of Credit"], num_samples),
    "Business_Investments": np.random.randint(5000, 500000, num_samples),
    "Sales_Tax_Obligations": np.random.randint(1000, 50000, num_samples),
    "Inventory_Method": np.random.choice(["FIFO", "LIFO", "Weighted Average"], num_samples),
    "Number_of_Employees": np.random.randint(1, 500, num_samples),
    "Employee_Salaries_&_Wages": np.random.randint(20000, 5000000, num_samples),
    "Bonuses_and_Incentives": np.random.randint(1000, 200000, num_samples),
    "Retirement_Contributions_for_Employees": np.random.randint(5000, 500000, num_samples),
    "Health_Benefits_Provided": np.random.randint(10000, 500000, num_samples),
}

# Convert dictionary to DataFrame
df = pd.DataFrame(data)

# Define Classification Labels
df["R&D_Credit_Eligible"] = np.where((df["R&D_Expenses"] > 0.05 * df["Gross_Revenue"]) | (df["R&D_Expenses"] > 50000), 1, 0)
df["ERC_Eligible"] = np.where((df["Payroll_Expenses"] > 0.2 * df["Gross_Revenue"]) & (df["Income_Growth_Rate"] < -0.2), 1, 0)
df["WOTC_Eligible"] = np.where((df["Number_of_Employees"] > 10) & (df["Payroll_Expenses"] > 500000), 1, 0)
df["Energy_Credit_Eligible"] = np.where(df["Energy_Efficiency_Credits"] > 0, 1, 0)
df["Home_Office_Eligible"] = np.where(df["Home_Office_Deduction"] > 0, 1, 0)

# Save to CSV
df.to_csv("synthetic_tax_optimization_data_v4.csv", index=False)

print("Synthetic dataset saved as 'synthetic_tax_optimization_data.csv' successfully!")
