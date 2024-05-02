from numpy.random import RandomState

from deampy.econ_eval import Strategy, CEA

# simulate 4 strategies with the following cost and effect normal distributions
dict_strategies = {
    #    mean cost, stdev cost, mean effect, stdev effect
    'O': [0,        0,          0,           0,      'green'],
    'A': [250000,   100000,     20,          7.5,    'blue'],
    'B': [500000,   100000,     10,          7.5,    'red'],
    'C': [750000,   100000,     25,          4,      'orange'],
    'D': [1250000,  150000,     40,          5,      'purple'],
}

# generate 1000 random sample for each strategy
n_sims = 200


# generate random samples for the cost and effect of each strategy and put them
# in a dictionary of costs and a dictionary of effects
rng = RandomState(0)
dict_cost_samples = {}  # dictionary of cost samples with strategy name as key
dict_effect_samples = {}  # dictionary of effect samples with strategy name as key
for s in dict_strategies:
    # samples from normal distributions of cost and effect
    dict_cost_samples[s] = rng.normal(dict_strategies[s][0], dict_strategies[s][1], n_sims)
    dict_effect_samples[s] = rng.normal(dict_strategies[s][2], dict_strategies[s][3], n_sims)


# create a list of strategies with the cost and effect samples to use in the cost-effectiveness (CE) analysis
list_strategies = []
for s in dict_strategies:
    s = Strategy(
        name=s,     # name of this strategy
        cost_obs=dict_cost_samples[s],  # cost observations for this strategy
        effect_obs=dict_effect_samples[s],  # effect observations for this strategy
        color=dict_strategies[s][4]  # color to use for this strategy in the CE plot
    )
    list_strategies.append(s)

# create an CEA object to conduct the CEA
cea = CEA(
    strategies=list_strategies,  # list of strategies to compare
    if_paired=True,  # cost and effect observations are assumed to be paired across strategies (see the paper)
    wtp_range=[0, 100000],  # range of willingness-to-pay values to use in the analysis
)

# create the plot of CE plane and net monetary benefit (NMB) lines
cea.plot_cep_nmb(
    fig_size=(8, 4),
    file_name='cep nmb N={}.png'.format(n_sims),
    cost_multiplier=0.001,
    nmb_multiplier=0.001,
    cep_y_label='Additional Cost (Thousand)',
    nmb_y_label='Incremental NMB (Thousand)',
    show_strategy_label_on_nmb_frontier=True,
)

# calculate minimum required number of parameter samples
cea.plot_min_monte_carlo_parameter_samples(
    max_wtp=200000,
    epsilons=[1000, 2000, 5000],
    alphas=[0.05],
    filename='min n.png'
)
