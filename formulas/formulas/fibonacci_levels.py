# formulas/fibonacci_levels.py
def calculate_fibonacci_levels(data):
    """Calculate Fibonacci retracement and extension levels."""
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
            '100.0%': round(min_price, 2),
            '123.6%': round(min_price - 0.236 * diff, 2),
            '138.2%': round(min_price - 0.382 * diff, 2),
            '161.8%': round(min_price - 0.618 * diff, 2),
            '200.0%': round(min_price - 1.0 * diff, 2),
            '261.8%': round(min_price - 1.618 * diff, 2)
        }
        return levels
    except (KeyError, ValueError) as e:
        print(f"Error calculating Fibonacci levels: {e}")
        return None
