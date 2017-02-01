from __future__ import division

from deap import base, creator, tools
import re
import requests
import pdb


sign = lambda x: '1' if x>0 else '0'


def load_product_url(fm_name):
    feature_names = []
    featureNum = 0
    cnfNum = 0
    cnfs = []

    feature_name_pattern = re.compile(r'c (\d+)\$? (\w+)')
    stat_line_pattern = re.compile(r'p cnf (\d+) (\d+)')

    features_names_dict = dict()
    source = requests.get('https://zenodo.org/record/265808/files/'+fm_name+'.dimacs').text.encode('ascii').split('\n')

    for line in source:
        if line.startswith('c'):  # record the feature names
            m = feature_name_pattern.match(line)
            """
            m.group(1) id
            m.group(2) name
            """
            features_names_dict[int(m.group(1))] = m.group(2)

        elif line.startswith('p'):
            m = stat_line_pattern.match(line)
            """
            m.group(1) feature number
            m.group(2) cnf
            """
            featureNum = int(m.group(1))
            cnfNum = int(m.group(2))

            # transfer the features_names into the list if dimacs file is valid
            assert len(features_names_dict) == featureNum, "There exists some features without any name"
            for i in range(1, featureNum+1):
                feature_names.append(features_names_dict[i])
            del features_names_dict

        elif line.endswith('0'):  # the cnf
            cnfs.append(map(int, line.split(' '))[:-1])  # delete the 0, store as the lint list

        else:
            assert True, "Unknown line" + line
    assert len(cnfs) == cnfNum, "Unmatched cnfNum."

    return feature_names, featureNum, cnfs, cnfNum


class DimacsModel:
    def __init__(self, fm_name):
        self.name = fm_name
        _, self.featureNum, self.cnfs, self.cnfNum = load_product_url(fm_name)

        self.cost = []
        self.used_before = []
        self.defects = []

        lines = requests.get('https://zenodo.org/record/265807/files/'+fm_name+'.dimacs.augment').text.encode('ascii')
        lines = lines.split('\n')[1:]
        lines = map(lambda x:x.rstrip(), lines)
        for l in lines:
            if not len(l): continue
            _, a, b, c = l.split(" ")
            self.cost.append(float(a))
            self.used_before.append(bool(int(b)))
            self.defects.append(int(c))

        creator.create("FitnessMin", base.Fitness, weights=[-1.0] * 5, vioconindex=list())
        creator.create("Individual", str, fitness=creator.FitnessMin)

        self.creator = creator
        self.Individual = creator.Individual

        self.toolbox = base.Toolbox()
        self.toolbox.register("evaluate", self.eval_ind)
        self.eval = self.toolbox.evaluate
    #
    # def get_random_bit_ind(self, background=None, mask=None):
    #     dec = ''
    #     if mask is None:
    #         mask = range(self.featureNum)
    #     for i in range(self.featureNum):
    #         if i in mask:
    #             dec += random.choice(['0', '1'])
    #         else:
    #             dec += background[i]
    #     return self.Individual(dec)
    #
    # def gen_random_bit_ind_r(self, pb=0.5):
    #     dec = ''
    #     for i in range(self.featureNum):
    #         if random.uniform(0,1) <= pb:
    #             dec += '1'
    #         else:
    #             dec += '0'
    #     return self.Individual(dec)
    #

    def eval_ind(self, ind, normalized=True):
        """
        return the fitness, but it might be no needed.
        Args:
            ind:

        Returns:

        """
        convio = 0
        ind.fitness.vioconindex = []
        for c_i, c in enumerate(self.cnfs):
            corr = False
            for x in c:
                if sign(x) == ind[abs(x)-1]:
                    corr = True
                    break
            if not corr:
                ind.fitness.vioconindex.append(c_i)
                convio += 1

        unselected, unused, defect, cost = 0, 0, 0, 0
        for i, selected in enumerate(map(int, ind)):
            if not selected:
                unselected += 1
            else:
                cost += self.cost[i]
                if self.used_before[i]:
                    defect += self.defects[i]
                else:
                    unused += 1
        if normalized:
            ind.fitness.values = (convio/self.cnfNum,
                                  unselected/self.featureNum,
                                  unused/self.featureNum,
                                  defect/sum(self.defects),
                                  cost/sum(self.cost))
        else:
            ind.fitness.values = (convio, unselected, unused, defect, cost)

    #
    # @staticmethod
    # def bit_flip_mutate(individual):
    #     # modification log -- not use the mutateRate parameter. just select one bit and flip that
    #     n = len(individual)
    #     i = random.randint(0, n-1)
    #     T = type(individual)
    #     if individual[i] == '0':
    #         individual = T(individual[:i]+'1'+individual[i+1:])
    #     del individual.fitness.values
    #     return individual,
    #
    # @staticmethod
    # def cxTwoPoint(ind1, ind2):
    #     v1 = list(ind1[:])
    #     v2 = list(ind2[:])
    #     split = random.randint(0, len(v1)-1)
    #     for i in range(split):
    #         v1[i], v2[i] = v2[i], v1[i]
    #     T = type(ind1)
    #     ind1 = T(''.join(v1))
    #     ind2 = T(''.join(v2))
    #     del ind1.fitness.values
    #     del ind2.fitness.values
    #     return ind1, ind2

if __name__ == '__main__':
    p = DimacsModel('webportal')
    # ind = p.Individual('1000111000000000010000000001111111000001100100000')
    # p.eval(ind)
    # pdb.set_trace()

