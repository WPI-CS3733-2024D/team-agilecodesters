import numpy as np
from scipy import stats

# Sample data from the Commercial and Residential bank branches
commercial_times = [
    4.21, 5.47, 3.06, 5.07, 4.55, 2.54, 3.38, 3.01,
    4.63, 6.16, 0.41, 5.05, 6.53, 6.46, 3.55
]
residential_times = [
    9.55, 5.78, 8.07, 5.65, 8.54, 3.72, 8.15, 8.46,
    10.57, 6.79, 5.41, 4.05, 6.23, 9.91, 5.37
]

# Calculating the t-statistic and p-value
t_stat, p_value = stats.ttest_ind(commercial_times, residential_times, equal_var=False)

print(t_stat)
print(p_value)