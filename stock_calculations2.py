import numpy as np

def calculate_moving_average(data, period, key='close'):
    """Calculate the moving average for the given period."""
    if not data or len(data['values']) < period:
        return None
    try:
        closes = [float(item[key]) for item in data['values'][:period]]
        return round(sum(closes) / len(closes), 2)
    except (KeyError, ValueError) as e:
        print(f"Error calculating moving average: {e}")
        return None

def calculate_slope(data, period, key='close'):
    """
    Calculate the slope of the moving average over the given period.
    Slope = (latest MA - earliest MA) over the window.
    """
    if not data or len(data['values']) < period + 1:
        return None
    try:
        moving_averages = []
        for i in range(len(data['values']) - period + 1):
            window = data['values'][i:i+period]
            closes = [float(item[key]) for item in window]
            ma = sum(closes) / len(closes)
            moving_averages.append(ma)
        # Slope: difference between last and first moving average in the window
        slope = moving_averages[-1] - moving_averages[0]
        return round(slope, 4)
    except (KeyError, ValueError) as e:
        print(f"Error calculating slope: {e}")
        return None

def calculate_fibonacci_levels(data):
    """Calculate Fibonacci retracement levels."""
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
    """Perform all stock calculations."""
    if not data or 'values' not in data:
        return None

    try:
        # Get the latest price and last 10 days' prices
        current_price = float(data['values'][-1]['close'])
        recent_prices = [float(entry['close']) for entry in data['values'][-10:]]

        # Calculate 200-week moving average
        ma_200_week = calculate_moving_average(data, 200 * 5)

        # Determine isInteresting
        is_interesting = any(price < ma_200_week for price in ([current_price] + recent_prices)) if ma_200_week else False
        
        return {
            '50_week_moving_average': calculate_moving_average(data, 50),
            '50_week_moving_average_slope': calculate_slope(data, 50),
            '200_week_moving_average': ma_200_week,
            '200_week_moving_average_slope': calculate_slope(data, 200),
            'fibonacci_levels': calculate_fibonacci_levels(data),
            #'rsi': calculate_rsi(data, 14),
            #'bollinger_bands': calculate_bollinger_bands(data, 20, 2),
            #'macd': calculate_macd(data, 12, 26, 9), 
            #'pivot_points': calculate_pivot_points(data),
            'isInteresting': is_interesting
        }
    except Exception as e:
        print(f"Error in perform_calculations: {e}")
        return None
