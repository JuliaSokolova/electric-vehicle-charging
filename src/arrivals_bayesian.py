import pymc3 as pm
import theano.tensor as tt
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from IPython.core.pylabtools import figsize


def calc_posteriors(data, n_data):
    '''
    Calculates posterior probablilities labda1, lambda2 and taus for data
    '''
    with pm.Model() as model:
        alpha = 1.0/data.mean()
        lambda_1 = pm.Exponential("lambda_1", alpha)
        lambda_2 = pm.Exponential("lambda_2", alpha)
        tau = pm.DiscreteUniform("tau", lower=0, upper=n_data - 1)

    with model:
        idx = np.arange(n_data)
        lambda_ = pm.math.switch(tau > idx, lambda_1, lambda_2)

    with model:
        observation = pm.Poisson("obs", lambda_, observed=data)

    with model:
        step = pm.Metropolis()
        trace = pm.sample(10000, step=step)

    lambda_1_samples = trace['lambda_1']
    lambda_2_samples = trace['lambda_2']
    tau_samples = trace['tau']

    return lambda_1_samples, lambda_2_samples, tau_samples

if __name__ == '__main__':
    # loading data
    charging = pd.read_csv('./data/charging.csv')
    msk = charging["ConnectionTime"].dt.year > 2019
    interval = charging[msk]
    data = interval["ConnectionTime"].groupby([
        interval["ConnectionTime"].dt.year,
        interval["ConnectionTime"].dt.month,
        interval["ConnectionTime"].dt.day]).count()
    n_data = len(data)

    # make a graph to eyeball if the variable changed
    fig, ax = plt.subplots(figsize=(16, 8))
    plt.bar(np.arange(n_data), data, color="magenta")
    plt.xlabel('Time days')
    plt.ylabel('Number of cars arrived')
    plt.title('Did the number of cars arrived change over time?')

    # calculating posteriors lambdas
    lambda_1_samples,
    lambda_2_samples,
    tau_samples = calc_posteriors(data, n_data)

    # plot posteriors
    plt.rcParams.update({'font.size': 16})
    figsize(16, 10)

    # histogram of the samples:
    ax = plt.subplot(211)
    ax.set_autoscaley_on(False)

    plt.hist(
        lambda_1_samples,
        bins=30,
        alpha=0.85,
        label="posterior of $\lambda_1$",
        color="#8ecd00",
        density=True)
    plt.legend(loc="upper left")
    plt.title(r"""Posterior distributions of the variables
        $\lambda_1$; $\lambda_2$""")
    plt.xlim([0, 30])
    plt.xlabel("$\lambda_1$ value")

    ax = plt.subplot(212)
    ax.set_autoscaley_on(False)
    plt.hist(
        lambda_2_samples,
        bins=10,
        alpha=0.85,
        label="posterior of $\lambda_2$",
        color="#7A68A6",
        density=True)
    plt.legend(loc="upper left")
    plt.xlim([0, 30])
    plt.xlabel("$\lambda_2$ value")

    # histogram of taus
    figsize(16, 4)
    ax = plt.subplot()
    w = 1.0 / tau_samples.shape[0] * np.ones_like(tau_samples)
    plt.hist(
        tau_samples,
        weights=w,
        label=r"posterior of $\tau$",
        color="black",
        rwidth=2)
    plt.xlabel(r"$\tau$ (in days)")
    plt.ylabel("probability")
    plt.legend(loc="upper left")

    # plot the results on top of the actual data
    figsize(16, 6)
    N = tau_samples.shape[0]
    expected_cars_per_day = np.zeros(n_data)
    for day in range(0, n_data):
        ix = day < tau_samples
        expected_cars_per_day[day] = (
            lambda_1_samples[ix].sum() +
            lambda_2_samples[~ix].sum()) / N
    plt.plot(
        range(n_data),
        expected_cars_per_day,
        lw=4,
        color="#cd6001",
        label="expected number of cars arrived")
    plt.xlim(0, n_data)
    plt.xlabel("Day")
    plt.ylabel("Expected # cars")
    plt.title("Expected number of cars arrived")
    plt.ylim(0, 60)
    plt.bar(
        np.arange(len(data)),
        data,
        color="#8ecd00",
        alpha=0.65,
        label="observed cars arrived")
    plt.legend(loc="upper left")
