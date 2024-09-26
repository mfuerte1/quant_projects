# Importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

# Black-Scholes formula for European call option pricing
def black_scholes_call(S, X, T, r, sigma):
    '''
    Calculate the Black-Scholes European Call Option Price
    S: Stock price
    X: Strike price
    T: Time to expiration (in years)
    r: Risk-free rate
    sigma: Volatility of underlying stock
    '''
    d1 = (np.log(S / X) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # Call price calculation using cumulative standard normal distribution
    call_price = S * norm.cdf(d1) - X * np.exp(-r * T) * norm.cdf(d2)
    return call_price

# Function to create confidence intervals for variance
def confidence_interval_variance(sample_variance, N, confidence_level=0.95):
    '''
    Calculate confidence intervals for the variance
    sample_variance: Variance from historical stock returns
    N: Number of observations
    confidence_level: Confidence level for the interval (default: 95%)
    '''
    alpha = 1 - confidence_level
    chi2_upper = np.percentile(np.random.chisquare(N-1, 10000), (1 - alpha/2) * 100)
    chi2_lower = np.percentile(np.random.chisquare(N-1, 10000), (alpha/2) * 100)
    
    lower_bound = (N-1) * sample_variance / chi2_upper
    upper_bound = (N-1) * sample_variance / chi2_lower
    
    return lower_bound, upper_bound

# Load sample stock and option data
# Simulated data: In a real case, load historical stock prices and options data.
np.random.seed(42)
stock_prices = np.linspace(100, 150, 50)  # Simulated stock prices
option_prices = np.random.normal(5, 1, 50)  # Simulated option prices
strike_price = 120  # Strike price for the option
time_to_expiration = 30 / 365  # Time to expiration in years
risk_free_rate = 0.05  # Risk-free rate (5%)
sample_variance = np.var(stock_prices)  # Sample variance of stock prices
N = len(stock_prices)

# Estimate the implied variance
implied_vol = np.sqrt(sample_variance) / 100

# Calculate confidence intervals for implied variance
lower_bound, upper_bound = confidence_interval_variance(sample_variance, N)

# Calculate the Black-Scholes price for the upper and lower variance
call_price_upper = black_scholes_call(stock_prices, strike_price, time_to_expiration, risk_free_rate, np.sqrt(upper_bound))
call_price_lower = black_scholes_call(stock_prices, strike_price, time_to_expiration, risk_free_rate, np.sqrt(lower_bound))

# Empirical test: Plot market option prices and Black-Scholes confidence intervals
plt.figure(figsize=(10, 6))
plt.plot(stock_prices, option_prices, label="Market Option Prices", marker='o', linestyle='None')
plt.plot(stock_prices, call_price_upper, label="Upper Bound Call Price (CI)", linestyle='--')
plt.plot(stock_prices, call_price_lower, label="Lower Bound Call Price (CI)", linestyle='--')
plt.fill_between(stock_prices, call_price_lower, call_price_upper, color='gray', alpha=0.3, label="Confidence Interval")
plt.xlabel("Stock Price")
plt.ylabel("Option Price")
plt.title("Market Prices vs. Black-Scholes Confidence Interval")
plt.legend()
plt.grid(True)
plt.show()
