import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import warnings

# Suppress warnings from distribution fitting
warnings.filterwarnings("ignore")

# Function to fit and return parameters for multiple distributions
def fit_distributions(data):
    distributions = {
        'Normal': stats.norm,
        'Log-Normal': stats.lognorm,
        'Beta': stats.beta,
        'Weibull': stats.weibull_min
    }
    fitted_params = {}
    x = np.linspace(min(data), max(data), 1000)
    pdfs = {}

    for name, dist in distributions.items():
        try:
            params = dist.fit(data)
            fitted_params[name] = params
            pdfs[name] = dist.pdf(x, *params)
        except Exception as e:
            fitted_params[name] = str(e)
            pdfs[name] = None

    return x, pdfs, fitted_params

# Function to simulate portfolio values
def simulate_portfolios(years, salary_schedule, mean_return, std_deviation, starting_capital, monthly_expenses, retirement_contribution_percent, employee_match_percent, num_simulations):
    def calculate_take_home_salary(salary):
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

    def calculate_annual_contribution(salary):
        monthly_take_home_salary, total_annual_retirement_contribution = calculate_take_home_salary(salary)
        monthly_savings = monthly_take_home_salary - monthly_expenses
        annual_contribution = total_annual_retirement_contribution + (monthly_savings * 12)
        return annual_contribution

    all_simulations = []
    for _ in range(num_simulations):
        portfolio_values = [starting_capital]
        for year in range(years):
            salary = salary_schedule[min(year, len(salary_schedule)-1)]
            annual_contribution = calculate_annual_contribution(salary)
            annual_return = np.random.normal(mean_return, std_deviation)
            new_value = portfolio_values[-1] * (1 + annual_return) + annual_contribution
            portfolio_values.append(new_value)
        all_simulations.append(portfolio_values)
    return np.array(all_simulations)

# Parameters
mean_return = 0.07
std_deviation = 0.15
num_simulations = 10000
starting_capital = 132000

starting_salary = 36000
target_salary = 50000
years_to_target = 5
post_target_growth_rate = 0.02
salary_ceiling = 600000
monthly_expenses = 1000
retirement_contribution_percent = 6
employee_match_percent = 9

# Evaluation years
evaluation_years = [15, 30, 45]

# Plotting
plt.figure(figsize=(18, 5))

for idx, total_years in enumerate(evaluation_years):
    # Generate salary schedule
    salary_schedule = []
    for year in range(total_years):
        if year < years_to_target:
            growth_factor = (target_salary / starting_salary) ** (1 / years_to_target)
            salary = starting_salary * (growth_factor ** year)
        else:
            salary = salary_schedule[-1] * (1 + post_target_growth_rate)
            salary = min(salary, salary_ceiling)
        salary_schedule.append(salary)

    # Simulate portfolios
    simulations = simulate_portfolios(total_years, salary_schedule, mean_return, std_deviation, starting_capital, monthly_expenses, retirement_contribution_percent, employee_match_percent, num_simulations)
    final_values = simulations[:, -1]

    # Fit distributions
    x, pdfs, fitted_params = fit_distributions(final_values)

    # Plot KDE and distribution fits
    plt.subplot(1, len(evaluation_years), idx + 1)
    sns_kde = stats.gaussian_kde(final_values)
    plt.plot(x, sns_kde(x), label='KDE', color='black', linewidth=2)

    colors = ['red', 'blue', 'orange', 'purple']
    for color, (name, pdf) in zip(colors, pdfs.items()):
        if pdf is not None:
            plt.plot(x, pdf, label=name, linestyle='--', color=color)

    plt.title(f'{total_years} Year Portfolio Distribution')
    plt.xlabel('Portfolio Value')
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True)

    # Print parameters
    print(f"\n--- {total_years} Years ---")
    for name, params in fitted_params.items():
        if isinstance(params, tuple):
            formatted = ', '.join([f"{p:.2e}" for p in params])
            print(f"{name} Parameters: {formatted}")
        else:
            print(f"{name} Fit Error: {params}")

plt.tight_layout()
plt.savefig("multi_distribution_fits.png")
plt.show()

