import numpy as np

def calculate_correlation(field):
    """
    Calculates the spatial correlation function G(r).
    """
    L = field.shape[0]
    corrs = np.zeros(L // 2)
    
    # We subtract the mean squared (connected correlation) to see decay to zero
    mean_phi_sq = np.mean(field)**2
    
    for r in range(L // 2):
        shifted_field = np.roll(field, shift=r, axis=0)
        corrs[r] = np.mean(field * shifted_field) - mean_phi_sq
        
    return corrs

def autocorrelation_function(series):
    """
    Calculates the normalized autocorrelation of a time series.
    """
    series = np.array(series)
    n = len(series)
    if n < 2: return np.array([1.0])
    
    mean = np.mean(series)
    var = np.var(series)
    if var == 0: return np.ones(n) # Handle constant series
    
    series_centered = series - mean
    res = np.correlate(series_centered, series_centered, mode='full')[n-1:]
    
    # Unbiased normalization
    norm = var * np.arange(n, 0, -1)
    return res / norm

def estimate_tau(series):
    """
    Estimates the integrated autocorrelation time using a Self-Consistent Window.
    """
    rho = autocorrelation_function(series)
    if len(rho) < 2: return 0.5
    
    # Wolff often decorrelates immediately
    if rho[1] < 0.01: 
        return 0.5
    
    # Madras-Sokal windowing: sum until the lag M > 5*tau
    # For simplicity, we use the "first negative" or "max window" approach
    limit = np.where(rho < 0)[0]
    max_window = min(len(rho), 1000)
    window = limit[0] if len(limit) > 0 else max_window
    
    return 0.5 + np.sum(rho[1:window])