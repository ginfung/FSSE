# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # Copyright (C) 2016, Jianfeng Chen <jchen37@ncsu.edu>
# # vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# #
# # Permission is hereby granted, free of charge, to any person obtaining a copy
# #  of this software and associated documentation files (the "Software"), to deal
# #  in the Software without restriction, including without limitation the rights
# #  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# #  copies of the Software, and to permit persons to whom the Software is
# #  furnished to do so, subject to the following conditions:
# #
# # The above copyright notice and this permission notice shall be included in
# #  all copies or substantial portions of the Software.
# #
# # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# #  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# #  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# #  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# #  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# #  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# #  THE SOFTWARE.
#
#
# from __future__ import division
# from __future__ import print_function
# from Benchmarks.SPL import DimacsModel
# from gmpy2 import popcount, mpz
# import time
# import sys
# import pycosat
# import random
# import copy
# import pdb
#
# def action(name):
#     fm = DimacsModel(name)
#
#     # pops = list()
#     cnf = copy.deepcopy(fm.cnfs)
#
#
#     f = open('/Users/jianfeng/Desktop/tse_rs/random/'+name+'.txt', 'w')
#
#     for _ in range(6):
#         start_at = time.time()
#         f.write('T: ' + str(start_at) + '\n')
#         while time.time()-start_at < 5*60:  # record every 5 mintutes
#             sol = pycosat.solve(cnf, vars=fm.featureNum)
#             if isinstance(sol, list):
#                 new_ind = fm.Individual(''.join(['1' if i > 0 else '0' for i in sol]))
#                 sys.stdout.write('.')
#                 # pops.append(new_ind)
#                 fm.eval(new_ind)
#                 f.write(' '.join(map(str, new_ind.fitness.values)))
#                 f.write('\n')
#                 cnf.append([-x for x in sol])
#             else:
#                 f.close()
#                 break
#         f.write('~~~\n')
#     f.close()
#
#     # with open('/Users/jianfeng/Desktop/tse_rs/'+name+'.txt', 'r') as f:
#     #     candidates = list()
#     #     for l in f:
#     #         candidates.append(l.strip('\n'))
#     #         if len(candidates) > 1000: break
#     #
#     # can = list()
#     # for i in candidates:
#     #     k = popcount(mpz(int(i,2)))
#     #     can.append((fm.Individual(i), k))
#     # del candidates
#     #
#     # can = sorted(can, key=lambda i:i[1])
#     # can = random.sample(can, 100)
#     #
#     # can = [i[0] for i in can]
#     # for i in can:
#     #     fm.eval(i)
#     #     # print(i.fitness.values)
#     #
#     # with open('/Users/jianfeng/Desktop/tse_rs/random/'+name+'.txt', 'w') as f:
#     #     for i in can:
#     #         f.write(' '.join(map(str, i.fitness.values)))
#     #         f.write('\n')
#
#
# if __name__ == '__main__':
#     models = ['linux']
#     # models = ['webportal', 'eshop',  'fiasco', 'freebsd', 'linux']
#     for model in models:
#         action(model)
#         print('finish ' + model)