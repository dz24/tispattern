import numpy as np
import matplotlib.pyplot as plt
import os

import scienceplots
plt.style.use('science')

# plt.rcParams.update({'font.size': 16})
# import matplotlib.font_manager as font_manager
# font = font_manager.FontProperties(size=13)
COLS0 = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']



def pattern(inp, outp, cap=250):
    a = np.loadtxt(inp)[:cap]
    min0 = min(a[:, 1])
    a[:,1] -= min0
    a[:,2] -= min0

    workers = list(set(a[:, 3]))
    min_ens, max_ens = min(a[:,0]), max(a[:,0])
    cols = ['C0', 'C1', 'C2',
            '#d62728', '#9467bd', '#8c564b', '#e377c2',
            '#7f7f7f', '#bcbd22', '#17becf']
    # c_dic = {0: 'r', 1: 'b', 2: 'g'}
    c_dic = {int(i): col for i, col in zip(list(range(int(max_ens))), COLS0)}
    # c_dic2 = {0: '#ffcccc', 1: '#ccccff', 2: '#cce5cc'}
    dic = {int(worker): None  for worker in workers}
    label_workers = []

    # plot worker end-> start |
    for worker in workers:
        if worker in (2.,):
            print('cheese')
            continue
        x = np.array([(i) for i in a if i[3] == int(worker)])
        time_ends = list(set([i[2] for i in x]))
        enss = {time: [] for time in time_ends}
        for time in time_ends:
            for i in x:
                if i[1] in time_ends:
                    enss[i[1]].append(i[0])
                if i[2] in time_ends:
                    enss[i[2]].append(i[0])
        for time in time_ends:
            if len(set(enss[time])) > 1:
                minmax = [min(enss[time]), max(enss[time])]
                plt.plot([time]*2, minmax, '--',
                         color=c_dic[int(worker)], alpha=0.4, linewidth='2.')
        dic[int(worker)] = time_ends

    # plot worker start -> end -
    for i in range(len(a)):
        worker = int(a[i][3])
        if worker in (2.,):
            print('cheese')
            continue
        if worker not in label_workers:
            plt.plot([a[i][1], a[i][2]], [a[i][0]]*2, color=c_dic[worker],
                     marker=5, label=f'Worker {worker+1}', linewidth='2.', markevery=[-1])
            # plt.arrow(a[i][1], a[i][0], a[i][2]-a[i][1], 0, color=c_dic[worker], linewidth=2.,
            #           length_includes_head=True, head_width=0.06, head_length=0.03,
            #           label=f'Worker {worker+1}')
            label_workers.append(worker)
        else:
            plt.plot([a[i][1], a[i][2]], [a[i][0]]*2, color=c_dic[worker],
                     marker=5, linewidth='2.', markevery=[-1])
            # plt.annotate(s='', xy=(a[i][2], [a[i][0]]), text=(a[i][1], [a[i][0]]), arrowprops=dict(arrowstyle='<->'), color=c_dic[worker], linewidth='2.')
            # print(a[i][1], a[i][0], a[i][2]-a[i][1], 0)
            # plt.arrow(a[i][1], a[i][0], a[i][2]-a[i][1], 0, color=c_dic[worker], linewidth='2.')
            # plt.arrow(a[i][1], a[i][0], a[i][2]-a[i][1], 0, color=c_dic[worker], linewidth=2., length_includes_head=True, head_width=0.06, head_length=0.03, overhang=-1.9)
            # plt.show()
            # exit('ape')

    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    plt.xlabel(r"Time")
    plt.ylabel(r"Path Ensemble")
    plt.xticks([])
    # yticks = ['[$0^{-}$] / T$_0$'] + [f'[{i}$^+$] / T$_{i+1}$' for i in range(int(max_ens))]
    yticks = ['[$0^{-}$]'] + [f'[{i}$^+$]' for i in range(int(max_ens))]
    # plt.yticks(yticks)
    plt.yticks(list(range(int(min_ens), int(max_ens)+1)), yticks)
    plt.minorticks_off()
    print(list(range(int(min_ens), int(max_ens)+1)))

    plt.ylim(top=7.25)
    plt.xlim(-0.1, 2.565)
    outpp = os.path.join(outp,'pattern8t_2.pdf')
    lgd = plt.legend(borderaxespad=0,  edgecolor='k',
                     ncol=3, loc="upper center",
                     bbox_to_anchor=(0.50, 0.975), prop={'size': 7}, frameon=True, facecolor='white', framealpha=1)
    lgd.get_frame().set_linewidth(0.5)
    plt.tick_params(left=False)
    # plt.show()
    # plt.xticks([])
    ax = plt.gca()
    ax.yaxis.set_ticks_position('left')
    plt.ylim(top=7.25)
    plt.ylim(bottom=-0.35)
    # ax.tick_params(axis=u'both', which=u'both',length=0)
    # ax.tick_params(top=False,
    #            bottom=False,
    #            left=False,
    #            right=False,
    #            labelleft=True)

    # ax = plt.gca()
    # handles, labels = ax.get_legend_handles_labels()
    # legend = ax.legend(handles, labels, loc='upper right', frameon=True, facecolor='k', edgecolor='k', framealpha=1)
# 
    # lgd = plt.legend(bbox_to_anchor=(0.50, 1.325), loc="upper center",
    #                  borderaxespad=0,  edgecolor='k', framealpha=1.0,)
    # lgd = plt.legend(bbox_to_anchor=(1.04, 0.5), loc="upper center",
    #                  borderaxespad=0,  edgecolor='k', framealpha=1.0,)
    # plt.show()
    # plt.savefig(outpp, bbox_extra_artists=(lgd,), bbox_inches='tight')
    # print(outpp)
    print(outpp)
    plt.savefig(outpp, bbox_inches='tight')

# pattern('../data/7ens_v2.txt', '../figs/')
pattern('../data/7ens.txt', '../figs/')
