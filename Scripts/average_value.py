import numpy as np
from statistics import harmonic_mean, geometric_mean

def means_and_std(values):
    
    """
    This function computes the vector of statistic and the indicator to set the tolerance.
    """
    if len(values) != 0:
        means = [np.mean(values), np.median(values), harmonic_mean(values), geometric_mean(values)]
        ranges = np.max(means) - np.min(means)
    else:
        means, ranges = np.nan, np.nan
    
    return means, ranges


def mean_intrinsic_value(values):
    
    """
    This function computes a representative number based on different statistic based on a tolerance metric.
    """
    
    if np.isnan(values).all():
        return np.nan
    else:
        value, means, ranges = 0, [], 0
        has_converged = False
        
        while not has_converged:
            means, ranges = means_and_std([x for x in values if ~np.isnan(x)])
            
            if np.isnan(means).all() or np.isnan(means).all():
                value = np.nan
            else:
                if ranges <= 10E-6:
                    has_converged = True
                    value = means[0]
                else:
                    values = means.copy()
        
        return value