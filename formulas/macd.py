from formulas.exponential_moving_average import calculate_exponential_moving_average  # Riutilizza EMA

def calculate_macd(data, short_period=12, long_period=26, signal_period=9, key='close'):
    """Calculate MACD line, signal line, and histogram."""
    if not data or len(data['values']) < long_period:
        return None
    try:
        # Per MACD, usiamo EMA completa su tutti i dati
        closes = [float(item[key]) for item in data['values']]
        ema_short = []
        ema_long = []
        for i in range(len(closes)):
            ema_short.append(calculate_exponential_moving_average({'values': data['values'][:i+1]}, short_period))
            ema_long.append(calculate_exponential_moving_average({'values': data['values'][:i+1]}, long_period))
        macd_line = [s - l for s, l in zip(ema_short, ema_long) if s is not None and l is not None]
        signal_line = calculate_exponential_moving_average({'values': [{'close': m} for m in macd_line]}, signal_period)
        histogram = macd_line[-1] - signal_line if signal_line else None
        return {
            'macd_line': round(macd_line[-1], 4),
            'signal_line': round(signal_line, 4) if signal_line else None,
            'histogram': round(histogram, 4) if histogram else None
        }
    except (KeyError, ValueError) as e:
        print(f"Error calculating MACD: {e}")
        return None
