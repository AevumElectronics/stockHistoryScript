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

def calculate_rsi(data, period=14):
    """Calculate Relative Strength Index (RSI)."""
    if not data or len(data['values']) < period + 1:
        return None
    try:
        closes = [float(item['close']) for item in data['values'][:period + 1]]
        gains = [max(closes[i] - closes[i + 1], 0) for i in range(len(closes) - 1)]
        losses = [max(closes[i + 1] - closes[i], 0) for i in range(len(closes) - 1)]
        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period
        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return round(rsi, 2)
    except (KeyError, ValueError) as e:
        print(f"Error calculating RSI: {e}")
        return None

def calculate_bollinger_bands(data, period=20, multiplier=2):
    """Calculate Bollinger Bands."""
    if not data or len(data['values']) < period:
        return None
    try:
        closes = [float(item['close']) for item in data['values'][:period]]
        sma = sum(closes) / period
        std_dev = np.std(closes)
        upper_band = sma + multiplier * std_dev
        lower_band = sma - multiplier * std_dev
        return {
            'middle_band': round(sma, 2),
            'upper_band': round(upper_band, 2),
            'lower_band': round(lower_band, 2)
        }
    except (KeyError, ValueError) as e:
        print(f"Error calculating Bollinger Bands: {e}")
        return None

def calculate_macd(data, short_period=12, long_period=26, signal_period=9):
    """Calculate MACD (Moving Average Convergence Divergence)."""
    if not data or 'values' not in data or len(data['values']) < long_period + signal_period:
        return None

    try:
        # Parse closes safely - ensure they are all floats
        closes = []
        for entry in data['values']:
            try:
                closes.append(float(entry['close']))
            except (ValueError, KeyError, TypeError):
                continue  # Skip malformed entries

        if len(closes) < long_period + signal_period:
            return None

        # Calculate EMAs
        def ema(prices, period):
            if not prices or len(prices) < period:
                return []
            
            alpha = 2 / (period + 1)
            ema_values = [prices[0]]  # Start with first price
            
            for price in prices[1:]:
                # Ensure price is a float
                try:
                    price_float = float(price)
                    ema_value = price_float * alpha + ema_values[-1] * (1 - alpha)
                    ema_values.append(ema_value)
                except (ValueError, TypeError):
                    continue
            
            return ema_values

        # Calculate short and long EMAs
        short_ema = ema(closes, short_period)
        long_ema = ema(closes, long_period)

        # Ensure we have enough data
        if len(short_ema) < long_period or len(long_ema) < long_period:
            return None

        # Align the EMAs (both should start from the same point)
        # Take the last len(long_ema) values from short_ema
        if len(short_ema) > len(long_ema):
            short_ema = short_ema[-len(long_ema):]
        
        # Calculate MACD line
        macd_line = [s - l for s, l in zip(short_ema, long_ema)]
        
        # Calculate signal line
        signal_line = ema(macd_line, signal_period)
        
        if not signal_line:
            return None

        # Calculate histogram
        # Align macd_line with signal_line
        aligned_macd = macd_line[-len(signal_line):]
        histogram = [m - s for m, s in zip(aligned_macd, signal_line)]

        return {
            'macd_line': round(macd_line[-1], 4),
            'signal_line': round(signal_line[-1], 4),
            'histogram': round(histogram[-1], 4)
        }

    except Exception as e:
        print(f"Error calculating MACD: {e}")
        return None

def calculate_pivot_points(data):
    """Calculate pivot points and support/resistance levels."""
    if not data or len(data['values']) < 1:
        return None
    try:
        latest = data['values'][0]  # Use the most recent day
        high = float(latest['high'])
        low = float(latest['low'])
        close = float(latest['close'])
        pivot = (high + low + close) / 3
        r1 = 2 * pivot - low
        s1 = 2 * pivot - high
        r2 = pivot + (high - low)
        s2 = pivot - (high - low)
        return {
            'pivot_point': round(pivot, 2),
            'resistance_1': round(r1, 2),
            'support_1': round(s1, 2),
            'resistance_2': round(r2, 2),
            'support_2': round(s2, 2)
        }
    except (KeyError, ValueError) as e:
        print(f"Error calculating pivot points: {e}")
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
            'rsi': calculate_rsi(data, 14),
            'bollinger_bands': calculate_bollinger_bands(data, 20, 2),
            'macd': calculate_macd(data, 12, 26, 9), 
            'pivot_points': calculate_pivot_points(data),
            'isInteresting': is_interesting
        }
    except Exception as e:
        print(f"Error in perform_calculations: {e}")
        return None
