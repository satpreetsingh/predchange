"""
Collection of functions used for generating various figures.
"""
from __future__ import division, print_function
from builtins import range

from numpy import arange, percentile, empty, object
from stats import neg_binomial

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

sns.set(context = 'talk', style = 'white', color_codes=True)
sns.set_palette(['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00'])

def make_figure_with_subplots():
    
    fig = plt.figure(figsize = (14,8))
    grids = GridSpec(ncols = 2, nrows =2)
    axes = empty((2,2), dtype = object)
    for i in range(2):
        for j in range(2):
            axes[i,j] = fig.add_subplot(grids[i,j])
    
    fig.subplots_adjust(wspace = .1, hspace = .3)
    
    return fig, axes

def plot_between_reversal_interval_distribution(axes):
    d_max = 50
    d = arange(d_max)
    mu = 20
    sigma = mu*(mu-1)
    p0 = neg_binomial(mu, sigma, d)
    axes[0].bar(arange(d_max)+1, p0, color = 'r', alpha = 0.5)
    
    sigma = mu
    p0 = neg_binomial(mu, sigma, d)
    axes[1].bar(arange(d_max)+1, p0, color = 'b', alpha = 0.5)

    axes[0].vlines(20, 0, 0.1, color = 'k', linestyle = '--', label = r'$\mu$')
    axes[1].vlines(20, 0, 0.1, color = 'k', linestyle = '--')
    
    axes[0].set_xlim([1,50])
    axes[1].set_xlim([1,50])
    axes[0].legend()
    axes[1].legend()

    axes[0].set_ylabel(r'$p_0(d)$')
    axes[1].set_ylabel(r'$p_0(d)$')
    axes[1].set_xlabel(r'$d$')
    
    sns.despine(ax=axes[0])
    sns.despine(ax=axes[1])
    
def plot_mean_performance_lines(axes, performance):
    means = arange(10,31)
    c = ['r', 'b']
    labels = ['IRI', 'RRI']
    for i in range(2):
        for j in range(2):
            axes[i].plot(means, percentile(performance[i,j], 50, axis = -1), c[j], label = labels[j])
            p95 = percentile(performance[i,j], 95, axis = -1)
            p05 = percentile(performance[i,j], 5, axis = -1)
            p75 = percentile(performance[i,j], 75, axis = -1)
            p25 = percentile(performance[i,j], 25, axis = -1)
            axes[i].fill_between(means, p75, p25, alpha = .3, color = c[j])
            axes[i].fill_between(means, p95, p05, alpha = .1, color = c[j])
            
    
    axes[1].legend()
    axes[0].set_ylabel('performance')
    axes[0].set_xlabel(r'$\mu$')
    axes[1].set_xlabel(r'$\mu$')
    axes[0].set_xlim([10, 30])
    axes[1].set_xlim([10, 30])
    axes[0].set_ylim([.5, 1.])
    axes[1].set_ylim([.5, 1.])
    axes[1].set_yticklabels([])
    
    axes[1].set_xticks([10, 15, 20, 25, 30])
    axes[0].set_xticks([10, 15, 20, 25, 30])

import pandas as pd    
def plot_mean_performance_boxplot(axes, performance, labels):
    
    for i in range(2):
        df = pd.DataFrame(data = performance[i].T, columns=labels)
        sns.boxplot(data = df, ax = axes[i],
                    width=0.5)
        sns.despine(ax=axes[i], bottom = True)
        
        axes[i].set_xlabel('agent')
        axes[i].set_ylim([.4, 1.])
    
    axes[0].set_ylabel('performance')
    axes[1].set_yticklabels([])
            
    
def plot_probability_correct_choice1(axes, choice_probability):
    c = ['#e41a1c', '#377eb8']
    rel_trial = arange(-10, 11)
    locs = [0, 10, 20]
    styles = [':', '-', '--']
    labels = [r'$\mu=10$', r'$\mu=20$', r'$\mu=30$']
    lines = []
    for i in range(2):
        axes[i].vlines(0, 0,1, color = 'k', linestyle = '--')
        axes[i].set_xlabel('relative trial number')
        axes[i].set_xlim([-10, 10])
#        sns.despine(axes[i])
        for j in range(2):
            for k in range(3):
                line,=axes[i].plot(rel_trial, 
                                     choice_probability[i,j,locs[k]],
                                     color = c[j],
                                     linestyle=styles[k],
                                     label = labels[k])
                lines.append(line)
    
    axes[1].set_yticklabels([])
    axes[0].set_ylabel('Pr(choice=correct)')
    
    legend1 = axes[0].legend(handles=lines[:3], title='IRI', fontsize = 10)
    legend2 = axes[1].legend(handles=lines[-3:], title='RRI', fontsize = 10)
    
    plt.setp(legend1.get_title(),fontsize=10)
    plt.setp(legend2.get_title(),fontsize=10)
    
    axes[1].set_xticks([-10, -5, 0, 5, 10])
    axes[0].set_xticks([-10, -5, 0, 5, 10])

def plot_probability_correct_choice2(axes, choice_probability, labels):
    rel_trial = arange(-10, 11)
    lines = []
    for i in range(2):
        axes[i].vlines(0, 0,1, color = 'k', linestyle = '--')
        axes[i].set_xlabel('relative trial number')
        axes[i].set_xlim([-10, 10])
        sns.despine(ax=axes[i])
        for j in range(4):
            line,=axes[i].plot(rel_trial, 
                                 choice_probability[i,j],
                                 label = labels[j])
            lines.append(line)
    
    axes[1].set_yticklabels([])
    axes[0].set_ylabel('Pr(choice=correct)')
    
    axes[0].legend(fontsize = 10)
    axes[1].legend(fontsize = 10)
    
    axes[1].set_xticks([-10, -5, 0, 5, 10])
    axes[0].set_xticks([-10, -5, 0, 5, 10])
     
def plot_stats(performance, choice_probability, boxplot = False):
    
    fig, axes = make_figure_with_subplots()
    
    if boxplot:
        labels = ['IRI', 'RRI', 'SU-RW', 'DU-RW']
        plot_mean_performance_boxplot(axes[0,:], performance, labels)
        plot_probability_correct_choice2(axes[1,:], choice_probability, labels)
        
    else:
        labels = [r'$\mu = 10$', r'$\mu = 20$', r'$\mu = 0$']
        plot_mean_performance_lines(axes[0,:], performance)
        plot_probability_correct_choice1(axes[1,:], choice_probability)
        
    axes[0,0].set_title('irregular reversals')
    axes[0,1].set_title('semi-regular reversals')
    
    return fig
