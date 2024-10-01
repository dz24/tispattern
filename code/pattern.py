import numpy as np
import matplotlib.pyplot as plt
import os
plt.rcParams.update({'font.size': 16})
import matplotlib.font_manager as font_manager
font = font_manager.FontProperties(size=13)



def pattern(inp, outp, cap=250):
    a = np.loadtxt(inp)[:cap]
    min0 = min(a[:, 1])
    a[:,1] -= min0
    a[:,2] -= min0
    
    workers = list(set(a[:, 3]))
    min_ens, max_ens = min(a[:,0]), max(a[:,0])
    cols = ['#1f77b4', '#ff7f0e', '#2ca02c',
            '#d62728', '#9467bd', '#8c564b', '#e377c2',
            '#7f7f7f', '#bcbd22', '#17becf']
    # c_dic = {0: 'r', 1: 'b', 2: 'g'}
    c_dic = {int(i): col for i, col in zip(list(range(int(max_ens))), cols)} 
    # c_dic2 = {0: '#ffcccc', 1: '#ccccff', 2: '#cce5cc'}
    dic = {int(worker): None  for worker in workers}
    label_workers = []

    # plot worker end-> start |
    for worker in workers:
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
        if worker not in label_workers:
            plt.plot([a[i][1], a[i][2]], [a[i][0]]*2, color=c_dic[worker],
                     marker=">", label=f'worker {worker}', linewidth='2.', markevery=[-1])
            label_workers.append(worker)
        else:
            plt.plot([a[i][1], a[i][2]], [a[i][0]]*2, color=c_dic[worker],
                     marker=">", linewidth='2.', markevery=[-1])

    plt.xlabel(r"Wall time")
    plt.ylabel(r"Ensemble")
    plt.xticks([])
    yticks = ['[$0^{-}$]'] + [f'[{i}$^+$]' for i in range(int(max_ens))]
    # plt.yticks(yticks)
    plt.yticks(list(range(int(min_ens), int(max_ens)+1)), yticks)

    plt.ylim(top=8.5)
    outpp = os.path.join(outp,'pattern_legend3.pdf')
    lgd = plt.legend(borderaxespad=0,  edgecolor='k', framealpha=1.0,
                     ncol=3, prop=font, loc="upper center",
                     bbox_to_anchor=(0.50, 0.975))
    # lgd = plt.legend(bbox_to_anchor=(0.50, 1.325), loc="upper center",
    #                  borderaxespad=0,  edgecolor='k', framealpha=1.0,)
    # lgd = plt.legend(bbox_to_anchor=(1.04, 0.5), loc="upper center",
    #                  borderaxespad=0,  edgecolor='k', framealpha=1.0,)
    plt.show()
    # plt.savefig(outpp, bbox_extra_artists=(lgd,), bbox_inches='tight')
    # plt.savefig(outpp, bbox_inches='tight')

pattern('../data/short_pattern2.txt', '../figs/')
