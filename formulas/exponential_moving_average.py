import numpy as np

def calculate_exponential_moving_average(data, period, key='close'):
    """Calculate the Exponential Moving Average (EMA) for the given period."""
    if not data or len(data['values']) < period:
        return None
    try:
        closes = np.array([float(item[key]) for item in data['values']], dtype=float)
        weights = np.exp(np.linspace(-1., 0., period))
        weights /= weights.sum()
        ema = np.convolve(closes, weights, mode='full')[:len(closes)]
        ema[:period-1] = ema[period-1]  # Fill initial values with the first EMA
        return round(ema[-1], 2)  # Return the latest EMA value
    except (KeyError, ValueError) as e:
        print(f"Error calculating EMA: {e}")
        return None
