import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as stats


# Parameters for financial planning
mean_return = 0.07
std_deviation = 0.15
num_simulations = 10000

# User's financial details
starting_capital = 135000
starting_salary = 40000
target_salary = 40001
years_to_target = 1
post_target_growth_rate = 0.001
salary_ceiling = 100000
total_years = 20
monthly_expenses = 1000
retirement_contribution_percent = 6
employee_match_percent = 9

# Function to generate salary schedule
def generate_salary_schedule(starting_salary, target_salary, years_to_target, post_target_growth_rate, salary_ceiling, total_years):
    salary_schedule = []
    for year in range(total_years):
        if year < years_to_target:
            growth_factor = (target_salary / starting_salary) ** (1 / years_to_target)
            salary = starting_salary * (growth_factor ** year)
        else:
            salary = salary_schedule[-1] * (1 + post_target_growth_rate)
            salary = min(salary, salary_ceiling)
        salary_schedule.append(salary)
    return salary_schedule

# Function to calculate take-home salary and retirement contributions
def calculate_take_home_salary(salary, retirement_contribution_percent, employee_match_percent):
    personal_allowance = 12570
    basic_rate_threshold = 50270
    higher_rate_threshold = 150000

    basic_rate = 0.20
    higher_rate = 0.40
    additional_rate = 0.45

    ni_primary_threshold = 12570
    ni_upper_earnings_limit = 50270
    ni_basic_rate = 0.12
    ni_higher_rate = 0.02

    retirement_contribution = salary * (retirement_contribution_percent / 100)
    employer_match = salary * (employee_match_percent / 100)

    if salary > 100000:
        personal_allowance -= min(personal_allowance, (salary - 100000) / 2)

    taxable_income = max(0, salary - personal_allowance - retirement_contribution)

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

    take_home_salary = salary - tax - ni - retirement_contribution
    monthly_take_home_salary = take_home_salary / 12
    total_retirement_contribution = (retirement_contribution + employer_match)

    return monthly_take_home_salary, total_retirement_contribution

# Function to calculate annual contribution
def calculate_annual_contribution(salary, monthly_expenses, retirement_contribution_percent, employee_match_percent):
    monthly_take_home_salary, total_annual_retirement_contribution = calculate_take_home_salary(salary, retirement_contribution_percent, employee_match_percent)
    monthly_savings = monthly_take_home_salary - monthly_expenses
    annual_contribution = total_annual_retirement_contribution + (monthly_savings * 12)
    return annual_contribution

# Function to run Monte Carlo simulation
def monte_carlo_simulation(years, mean_return, std_deviation, starting_capital, salary_schedule, monthly_expenses, retirement_contribution_percent, employee_match_percent, num_simulations):
    all_simulations = []
    for _ in range(num_simulations):
        portfolio_values = [starting_capital]
        for year in range(years):
            salary = salary_schedule[year]
            annual_contribution = calculate_annual_contribution(salary, monthly_expenses, retirement_contribution_percent, employee_match_percent)
            annual_return = np.random.normal(mean_return, std_deviation)
            new_value = portfolio_values[-1] * (1 + annual_return) + annual_contribution
            portfolio_values.append(new_value)
        all_simulations.append(portfolio_values)
    return np.array(all_simulations)

# Function to plot summary statistics only
def plot_simulation_summary(simulations, years):
    plt.figure(figsize=(12, 6))

    mean_values = np.mean(simulations, axis=0)
    median_values = np.median(simulations, axis=0)
    q1_values = np.percentile(simulations, 25, axis=0)
    q3_values = np.percentile(simulations, 75, axis=0)
    p10_values = np.percentile(simulations, 10, axis=0)
    p90_values = np.percentile(simulations, 90, axis=0)

    x = range(years + 1)
    plt.plot(x, mean_values, label='Mean', color='green', linestyle='--')
    plt.plot(x, median_values, label='Median', color='red')
    plt.fill_between(x, q1_values, q3_values, color='gray', alpha=0.4, label='IQR (25th-75th)')
    plt.fill_between(x, p10_values, p90_values, color='blue', alpha=0.2, label='10th-90th Percentile')

    plt.title(f'Monte Carlo Simulation Summary for {years} Years')
    plt.xlabel('Year')
    plt.ylabel('Portfolio Value')
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.show()

# Function to plot annual contributions
def plot_annual_contributions(salary_schedule, monthly_expenses, retirement_contribution_percent, employee_match_percent):
    contributions = []
    for salary in salary_schedule:
        annual_contribution = calculate_annual_contribution(salary, monthly_expenses, retirement_contribution_percent, employee_match_percent)
        contributions.append(annual_contribution)

    plt.figure(figsize=(10, 5))
    plt.bar(range(1, len(contributions) + 1), contributions, color='skyblue')
    plt.title('Annual Investment Contributions (Excluding Returns)')
    plt.xlabel('Year')
    plt.ylabel('Annual Contribution (£)')
    plt.grid(True, axis='y', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()

# Generate salary schedule and run simulation
salary_schedule = generate_salary_schedule(starting_salary, target_salary, years_to_target, post_target_growth_rate, salary_ceiling, total_years)
simulations = monte_carlo_simulation(total_years, mean_return, std_deviation, starting_capital, salary_schedule, monthly_expenses, retirement_contribution_percent, employee_match_percent, num_simulations)

# Plot results
plot_simulation_summary(simulations, total_years)
plot_annual_contributions(salary_schedule, monthly_expenses, retirement_contribution_percent, employee_match_percent)

