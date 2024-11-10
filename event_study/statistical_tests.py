# event_study/statistical_tests.py

import numpy as np
from scipy import stats

def run_tests(data, num_permutations=1000):
    """
    执行t检验和三种非参数检验：
    - Wilcoxon符号秩检验
    - 单变量符号检验（Binomial Sign Test）
    - 广义符号检验（Permutation Test）

    返回一个包含所有检验统计量和P值的字典。
    """
    results = {}
    unique_data = np.unique(data)

    # T检验
    if len(unique_data) > 1:
        t_stat, t_p = stats.ttest_1samp(data, 0, nan_policy='omit')
        results['t_statistic'] = t_stat
        results['t_p_value'] = t_p
    else:
        results['t_statistic'] = np.nan
        results['t_p_value'] = np.nan

    # 非参数检验
    if len(unique_data) > 1:
        # Wilcoxon符号秩检验
        try:
            if np.all(data == 0):
                results['wilcoxon_statistic'] = np.nan
                results['wilcoxon_p_value'] = np.nan
            else:
                wilcoxon_stat, wilcoxon_p = stats.wilcoxon(data, zero_method='wilcox', correction=False, alternative='two-sided')
                results['wilcoxon_statistic'] = wilcoxon_stat
                results['wilcoxon_p_value'] = wilcoxon_p
        except:
            results['wilcoxon_statistic'] = np.nan
            results['wilcoxon_p_value'] = np.nan

        # 单变量符号检验
        num_positive = np.sum(data > 0)
        total = len(data)
        if total > 0:
            binom_result = stats.binomtest(num_positive, n=total, p=0.5, alternative='two-sided')
            results['binomial_statistic'] = binom_result.statistic
            results['binomial_p_value'] = binom_result.pvalue
        else:
            results['binomial_statistic'] = np.nan
            results['binomial_p_value'] = np.nan

        # 广义符号检验
        if total > 0:
            permuted_means = []
            for _ in range(num_permutations):
                permuted_data = np.random.choice([1, -1], size=total) * data
                permuted_mean = np.mean(permuted_data)
                permuted_means.append(permuted_mean)
            observed_mean = np.mean(data)
            permuted_means = np.array(permuted_means)
            p_value_perm = np.mean(np.abs(permuted_means) >= np.abs(observed_mean))
            results['permutation_statistic'] = observed_mean
            results['permutation_p_value'] = p_value_perm
        else:
            results['permutation_statistic'] = np.nan
            results['permutation_p_value'] = np.nan
    else:
        results['wilcoxon_statistic'] = np.nan
        results['wilcoxon_p_value'] = np.nan
        results['binomial_statistic'] = np.nan
        results['binomial_p_value'] = np.nan
        results['permutation_statistic'] = np.nan
        results['permutation_p_value'] = np.nan

    return results
