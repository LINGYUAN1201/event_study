import numpy as np
from scipy import stats

def patell_z_test(data):
    """Patell Z 检验"""
    if len(data) < 2:
        return np.nan, np.nan
    standardized_data = (data - np.mean(data)) / np.std(data, ddof=1)
    z_stat = np.sum(standardized_data) / np.sqrt(len(data))
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    return z_stat, p_value

def corrado_signed_rank_test(data):
    """Corrado 符号秩检验"""
    if len(data) < 2:
        return np.nan, np.nan
    ranks = stats.rankdata(abs(data))
    signed_ranks = np.sign(data) * ranks
    z_stat = np.sum(signed_ranks) / np.sqrt(np.sum(ranks**2))
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    return z_stat, p_value

def run_tests(data, num_permutations=1000):
    """执行统计检验并返回结果字典"""
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

    # Patell Z 检验
    patell_z_stat, patell_p_value = patell_z_test(data)
    results['patell_statistic'] = patell_z_stat
    results['patell_p_value'] = patell_p_value

    # Wilcoxon 符号秩检验
    try:
        if np.all(data == 0):
            results['wilcoxon_statistic'] = np.nan
            results['wilcoxon_p_value'] = np.nan
        else:
            wilcoxon_stat, wilcoxon_p = stats.wilcoxon(data, zero_method='wilcox', correction=False, alternative='two-sided')
            results['wilcoxon_statistic'] = wilcoxon_stat
            results['wilcoxon_p_value'] = wilcoxon_p
    except Exception as e:
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

    # 广义符号检验（Permutation Test）
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

    # Corrado 符号秩检验
    corrado_z_stat, corrado_p_value = corrado_signed_rank_test(data)
    results['corrado_statistic'] = corrado_z_stat
    results['corrado_p_value'] = corrado_p_value

    return results