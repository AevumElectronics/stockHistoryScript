# stock_calculations.py
def calculate_moving_average(data, period, key='close'):
    """Calculate the moving average for the given period using the specified key (e.g., 'close')."""
    if not data or len(data['values']) < period:
        return None
    try:
        closes = [float(item[key]) for item in data['values'][:period]]  # Use most recent 'period' values
        return round(sum(closes) / len(closes), 2)
    except (KeyError, ValueError) as e:
        print(f"Error calculating moving average: {e}")
        return None

def calculate_fibonacci_levels(data):
    """Calculate Fibonacci retracement levels based on the highest high and lowest low."""
    if not data or len(data['values']) < 2:
        return None
    try:
        highs = [float(item['high']) for item in data['values']]
        lows = [float(item['low']) for item in data['values']]
        max_price = max(highs)
        min_price = min(lows)
        diff = max_price - min_price
        levels = {
            '0.0%': round(max_price, 2),
            '23.6%': round(max_price - 0.236 * diff, 2),
            '38.2%': round(max_price - 0.382 * diff, 2),
            '50.0%': round(max_price - 0.5 * diff, 2),
            '61.8%': round(max_price - 0.618 * diff, 2),
            '100.0%': round(min_price, 2)
        }
        return levels
    except (KeyError, ValueError) as e:
        print(f"Error calculating Fibonacci levels: {e}")
        return None

def perform_calculations(data):
    """Perform all calculations and return them in a dictionary."""
    if not data or 'values' not in data:
        return None
    return {
        '50_day_moving_average': calculate_moving_average(data, 50),
        '200_week_moving_average': calculate_moving_average(data, 200 * 5),  # Approx 200 weeks in trading days
        'fibonacci_levels': calculate_fibonacci_levels(data)
    }
