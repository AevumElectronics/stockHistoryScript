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
