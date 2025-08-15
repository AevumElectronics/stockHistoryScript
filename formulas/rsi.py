import numpy as np

def calculate_rsi(data, period=14, key='close'):
    """Calculate the Relative Strength Index (RSI)."""
    if not data or len(data['values']) < period + 1:
        return None
    try:
        closes = np.array([float(item[key]) for item in data['values']])
        deltas = np.diff(closes)
        gain = np.maximum(deltas, 0)
        loss = np.abs(np.minimum(deltas, 0))
        avg_gain = np.mean(gain[:period])
        avg_loss = np.mean(loss[:period])
        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi = [100 - (100 / (1 + rs))]
        for i in range(period, len(deltas)):
            curr_gain = gain[i]
            curr_loss = loss[i]
            avg_gain = (avg_gain * (period - 1) + curr_gain) / period
            avg_loss = (avg_loss * (period - 1) + curr_loss) / period
            rs = avg_gain / avg_loss if avg_loss != 0 else 0
            rsi.append(100 - (100 / (1 + rs)))
        return round(rsi[-1], 2)  # Latest RSI
    except (KeyError, ValueError) as e:
        print(f"Error calculating RSI: {e}")
        return None
