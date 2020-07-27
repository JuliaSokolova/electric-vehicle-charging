import pandas as pd
from scipy import stats
import numpy as np


def find_smarts(users, charging):
    '''
    Filters tables user, charging to Smart RD cars
    '''
    max_request = charging[
        ['userID', 'kWhDelivered']].groupby(charging.userID).max()
    msk_Smart_1 = (max_request.kWhDelivered < 16.5)
    smarts_ID_1 = max_request[msk_Smart_1].userID
    msk_Smart_2 = (
        (max_WhPerMile.WhPerMile < 340) &
        (min_WhPerMile.WhPerMile > 300))
    smarts_ID_2 = max_WhPerMile[msk_Smart_2].userID
    # selecting smarts in charging
    smarts_mask_1 = charging.userID.isin(smarts_ID_1)
    smarts_charging = charging[smarts_mask_1]
    smarts_mask_2 = smarts_charging.userID.isin(smarts_ID_2)
    smarts_charging = smarts_charging[smarts_mask_2]
    # selectint smarts in users
    smarts_mask_u_1 = users.userID.isin(smarts_ID_1)
    smarts_users = users[smarts_mask_u_1]
    smarts_mask_u_2 = smarts_users.userID.isin(smarts_ID_2)
    smarts_users = smarts_users[smarts_mask_u_2]
    return smarts_charging, smarts_users


def bootstrap_mean(data, n_samples=10000):
    '''
    Calculates means for bootstrapped sample
    '''
    bootsrtap_means = []
    for i in range(n_samples):
        bootstrap_sample = np.random.choice(data, size=len(data), replace=True)
        bootsrtap_means.append(np.mean(bootstrap_sample))
    return bootsrtap_means

if __name__ == '__main__':
    users = pd.read_csv('./data/users.csv')
    charging = pd.read_csv('./data/charging.csv')
    smarts_charging, smarts_users = find_smarts(users, charging)

    # Using bootstrapping to check means distributions
    # for smart drivers miles requests
    all_data = list(smarts_users.milesRequested)
    all_boot_means = bootstrap_mean(all_data)
    all_var = np.var(all_data)
    all_var_boot = np.var(all_boot_means)
    boot_mean = np.mean(all_boot_means)
    print(f'All Smart users bootsrtap sample mean: {boot_mean_kWh}')
    print(f'Variance of all Smart users charge request: {all_var_kWh}')
    print(f'Variance of all Smart users means: {all_var_boot_kWh}')

    # finding bootsrtap confidence interval for the sample mean
    left = np.percentile(all_kWh_boot_means, 15)
    right = np.percentile(all_kWh_boot_means, 85)
    print('Confidence interval:', left, right)

    # Using bootstrapping to check out means distributions
    # for Smarts kWhDelivered
    all_data_kWhDelivered = list(smarts_charging.kWhDelivered)
    all_kWhDelivered_boot_means = bootstrap_mean(all_data_kWhDelivered)

    # Variance of bootstrapped means
    # for all smart users sessions (kWhDelivered)
    all_var_kWh = np.var(all_data_kWhDelivered)
    all_var_boot_kWh = np.var(all_kWhDelivered_boot_means)
    boot_mean_kWh = np.mean(all_kWhDelivered_boot_means)
    print(f'All Smart kWhDelivered bootsrtap sample mean: {boot_mean_kWh}')
    print(f'Variance of all Smart  kWhDelivered: {all_var_kWh}')
    print(f'Variance of all Smart kWhDelivered means: {all_var_boot_kWh}')
    # Finding bootsrtap confidence interval for the sample mean
    left = np.percentile(all_kWhDelivered_boot_means, 15)
    right = np.percentile(all_kWhDelivered_boot_means, 85)
    print('Confidence interval:', left, right)
