import numpy as np
from formulas.moving_average import calculate_moving_average

def calculate_bollinger_bands(data, period=20, std_dev=2, key='close'):
    """Calculate Bollinger Bands."""
    if not data or len(data['values']) < period:
        return None
    try:
        closes = [float(item[key]) for item in data['values'][-period:]]  # Ultimi 'period' giorni
        sma = calculate_moving_average({'values': data['values'][-period:]}, period)
        std = np.std(closes)
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        return {
            'middle_band': round(sma, 2),
            'upper_band': round(upper_band, 2),
            'lower_band': round(lower_band, 2)
        }
    except (KeyError, ValueError) as e:
        print(f"Error calculating Bollinger Bands: {e}")
        return None
