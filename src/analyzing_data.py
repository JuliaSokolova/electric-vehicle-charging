import pandas as pd
from matplotlib import pyplot as plt
from scipy import stats
import numpy as np
import seaborn as sns
import plotly.express as px


def avg_reguest_by_hour(hour, df=users):
    '''
    Calculates average size of charging requests for each hour
    '''
    users_new = users[users.kWhRequested <= 90]
    new_df = users_new[users_new.Modified.dt.hour == hour]
    avg_charge_request = new_df.kWhRequested.mean()
    return avg_charge_request


def avg_requests(ls):
    '''
    Calculats avg requests for all hours in the list
    '''
    result = []
    for i in ls:
        result.append(avg_reguest_by_hour(i))
    return result

if __name__ = '__main__':
    users = pd.read_csv('./data/users.csv')
    charging = pd.read_csv('./data/charging.csv')
    hours = = list(range(24))

    # prints general information about the dataset
    print(f'''This dataset has information about {users.nunique()}
              unique users and {charging.nunique()} charging sessions.''')
    print(f'''Time period: {charging.ConnectionTime.max()} -
              {charging.ConnectionTime.min()}''')

    # generates a graph of the total number of charging sessions for each month
    plt.rcParams.update({'font.size': 16})
    fig, ax = plt.subplots(figsize=(16, 4))
    ax = (charging["ConnectionTime"].groupby([
        charging["ConnectionTime"].dt.year,
        charging["ConnectionTime"].dt.month])
        .count().plot(kind="bar", figsize=(16, 6), color="#8ecd00"))
    ax.set_xlabel('Date: year, month')
    ax.set_ylabel('Number of charging sessions occured')
    ax.set_title('Charging sessions per month, 2018 - 2020')

    # generates a graph of the total number
    # of charging sessions for each day of the week
    plt.rcParams.update({'font.size': 16})
    fig, ax = plt.subplots(figsize=(16, 6))
    ax = (charging["ConnectionTime"].groupby([
        charging["ConnectionTime"].dt.weekday])
        .count().plot(kind="bar", figsize=(16, 6), color="#8ecd00"))
    ax.set_xlabel('Day of the week')
    ax.set_ylabel('Number of charging sessions')
    ax.set_ylim(1000, 6000)
    ax.set_title('Charging sessions per day, Monday - Sunday')

    # plot avarage size of charging requests for each hour of car arrival
    requests = avg_requests(hours)
    plt.rcParams.update({'font.size': 16})
    ax, fig = plt.subplots(figsize=(16, 6))
    ax = sns.barplot(x=hours, y=requests, color="#8ecd00")
    ax.set_ylabel('kWh')
    ax.set_xlabel('Time of arrival')
    ax.set_title('Average charge request for one car')
