import matplotlib.pyplot as plt
import numpy as np

# Function to calculate take-home salary, tax, and NI
def calculate_take_home_salary(salary):
    personal_allowance = 12570
    basic_rate_threshold = 50270
    higher_rate_threshold = 150000
    additional_rate_threshold = float('inf')
    
    basic_rate = 0.20
    higher_rate = 0.40
    additional_rate = 0.45
    
    ni_primary_threshold = 12570
    ni_upper_earnings_limit = 50270
    ni_basic_rate = 0.12
    ni_higher_rate = 0.02

    if salary > 100000:
        personal_allowance -= min(personal_allowance, (salary - 100000) / 2)
    
    taxable_income = max(0, salary - personal_allowance)
    
    if taxable_income <= basic_rate_threshold:
        tax = taxable_income * basic_rate
    elif taxable_income <= higher_rate_threshold:
        tax = (basic_rate_threshold * basic_rate) + ((taxable_income - basic_rate_threshold) * higher_rate)
    else:
        tax = (basic_rate_threshold * basic_rate) + ((higher_rate_threshold - basic_rate_threshold) * higher_rate) + ((taxable_income - higher_rate_threshold) * additional_rate)
    
    if salary <= ni_primary_threshold:
        ni = 0
    elif salary <= ni_upper_earnings_limit:
        ni = (salary - ni_primary_threshold) * ni_basic_rate
    else:
        ni = (ni_upper_earnings_limit - ni_primary_threshold) * ni_basic_rate + (salary - ni_upper_earnings_limit) * ni_higher_rate
    
    take_home_salary = salary - tax - ni
    monthly_take_home_salary = take_home_salary / 12
    monthly_tax = tax / 12
    monthly_ni = ni / 12

    return monthly_take_home_salary, monthly_tax, monthly_ni

salaries = [i for i in range(12570, 146001, 1)]

take_home_salaries = []
taxes = []
nis = []

for salary in salaries:
    take_home, tax, ni = calculate_take_home_salary(salary)
    take_home_salaries.append(take_home)
    taxes.append(tax)
    nis.append(ni)

plt.figure(figsize=(10, 6))
plt.stackplot(
    salaries,
    take_home_salaries,
    taxes,
    nis,
    labels=['Take Home', 'Tax', 'NI'],
    colors=['#4CAF50', '#F44336', '#2196F3']
)
plt.xlabel('Annual Gross Salary (£)')
plt.ylabel('Monthly Amount (£)')
plt.title('Monthly Take Home, Tax, and NI vs Annual Gross Salary')
plt.legend(loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()

#plt.figure(figsize=(10, 6))
#percent_take_home = [(th / (th + t + n) * 100) if (th + t + n) != 0 else 0 for th, t, n in zip(take_home_salaries, taxes, nis)]
#percent_tax = [(t / (th + t + n) * 100) if (th + t + n) != 0 else 0 for th, t, n in zip(take_home_salaries, taxes, nis)]
#percent_ni = [(n / (th + t + n) * 100) if (th + t + n) != 0 else 0 for th, t, n in zip(take_home_salaries, taxes, nis)]
#plt.plot(salaries, percent_take_home, label='Take Home %', color='#4CAF50')
#plt.plot(salaries, percent_tax, label='Tax %', color='#F44336')
#plt.plot(salaries, percent_ni, label='NI %', color='#2196F3')
#plt.xlabel('Annual Gross Salary (£)')
#plt.ylabel('Percentage (%)')
#plt.title('Percentage of Take Home, Tax, and NI vs Annual Gross Salary')
#plt.legend(loc='upper left')
#plt.grid(True)
#plt.tight_layout()
#plt.show()
