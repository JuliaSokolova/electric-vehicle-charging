import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns


def max_likelihood_by_hour(hour, df=charging):
    '''
    Calculates maximum likelehood for each hour
    '''
    new_df = charging[charging.ConnectionTime.dt.hour == hour]
    groupped = new_df.groupby([
        new_df.ConnectionTime.dt.year,
        new_df.ConnectionTime.dt.month,
        new_df.ConnectionTime.dt.day]).count()
    return groupped['_id'].mean()


def likelihoods(ls):
    '''Calculates likelihoods for several hours
    '''
    result = []
    for i in ls:
        result.append(all_arrivals_by_hour(i))
    return result

if __name__ == '__main__':
    users = pd.read_csv('./data/users.csv')
    charging = pd.read_csv('./data/charging.csv')
    hours = list(range(24))
    hourly_likelihoods = likelihoods(hours)
    plt.rcParams.update({'font.size': 16})
    ax, fig = plt.subplots(figsize=(16, 8))
    ax = sns.barplot(x=hours, y=hourly_likelihoods, color="#8ecd00")
    ax.set_ylabel('Cars per hour')
    ax.set_xlabel('Time of day')
    ax.set_title(
        'Number of cars arriving each hour (maximum likelihood estimation)')
