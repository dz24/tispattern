import numpy as np
import matplotlib.pyplot as plt
import os
# plt.rcParams.update({'font.size': 16})

import scienceplots
plt.style.use(["science"])
cols = [u'#1f77b4', u'#ff7f0e', u'#2ca02c', u'#d62728',
        u'#9467bd', u'#8c564b', u'#e377c2', u'#7f7f7f',
        u'#bcbd22', u'#17becf']

def tis(inp, outp, cap=250):
    # c_dic = {0: 'r', 1: 'b', 2: 'g'}
    a = np.loadtxt(inp)[:cap]
    enss_idx = list(set(a[:, 0]))
    c_dic = {int(i): col for i, col in zip(list(range(len(enss_idx))), cols)} 
    enss = {i: {'s':[], 'e':[]} for i in range(len(enss_idx))}
    diffs = []
    for idx, i in enumerate(a):
        if abs(i[2] - i[1]) not in diffs:
            diffs.append(abs(i[2] - i[1]))
        else:
            continue
        if len(enss[i[0]]['s']) == 0:
            enss[i[0]]['s'].append(0)
            enss[i[0]]['e'].append(abs(i[2] - i[1]))
        else:
            enss[i[0]]['s'].append(enss[i[0]]['e'][-1])
            enss[i[0]]['e'].append(abs(i[2] - i[1]) + enss[i[0]]['e'][-1])

    end = 0
    for i in range(len(enss[0.0]['s'])):
        idx = i%8
        s = enss[idx]['s'][0]
        e = enss[idx]['e'][0]
        plt.plot([s+end, e+end], [idx]*2, color=c_dic[0],
                     linewidth='2.', marker=">", markevery=[-1])
        if i != 0 and idx == 0:
            plt.plot([end]*2, [enss_idx[0], enss_idx[-1]], '--',
                      color=c_dic[0], alpha=0.4, linewidth='2.')
        end += e

    lgd = plt.legend(borderaxespad=0,  edgecolor='k', framealpha=1.0,
                     # ncol=3, prop=font, loc="upper center",
                     ncol=3, loc="upper center",
                     bbox_to_anchor=(0.50, 0.975))
    # for idx in enss_idx:
    #     for s, e in zip(enss[idx]['s'], enss[idx]['e']):
    #         plt.plot([s, e], [idx]*2, color=c_dic[int(idx)],
    #                  linewidth='2.', marker=">")
    print(enss_idx)
    # print(a)
    plt.xlim([0, 6.8])
    plt.xlabel(r"Wall time")
    plt.ylabel(r"Ensemble")
    plt.xticks([])
    plus = [f'$[{i}^+]$' for i in range(7)]
    plt.yticks(list(range(8)), [r'$[0^-]$'] + plus)
    plt.ylim(top=8.5)
    # plt.show()
    outpp = os.path.join(outp,'retis_pattern_ws0.pdf')
    plt.savefig(outpp, bbox_inches='tight')
    # plt.show()


tis('../data/long_pattern1.txt', '../figs/')
