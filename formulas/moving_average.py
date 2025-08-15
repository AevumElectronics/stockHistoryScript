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
