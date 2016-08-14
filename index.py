#!/usr/bin/python
from numpy.linalg import inv, slogdet, matrix_rank
from numpy import zeros
import itertools
import json
from fractions import Fraction
import pdb

# import sys

class EquilibriumComponent:
    def __init__(self, extreme_equilibria):
        self.extreme_equilibria = extreme_equilibria

    def index(self):
        index = 0
        for equilibrium in self.extreme_equilibria:
            index += equilibrium.lex_index
        return index

class Equilibrium:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lex_index = self.get_lex_index()

    def get_lex_index(self):
        lex_index = 0
        x_bases = self.x.lexico_feasible_bases
        y_bases = self.y.lexico_feasible_bases
        for alpha in x_bases:
            for beta in y_bases:

                pair = PairOfLexicoFeasibleBases(alpha, beta)
                if pair.fulfils_complementarity:
                    lex_index += pair.sign()
        return lex_index

class Strategy:
    def __init__(self, player, distribution, payoff, number):
        self.player = player
        self.payoff = payoff
        self.number = number
        self.number_of_pure_strategies = m if player == 1 else n
        self.opponent_number_of_pure_strategies = n if player == 1 else m
        self.distribution = distribution
        self.support = self.get_support()
        self.lexico_feasible_bases = self.get_bases()

    def get_support(self):
        result = []
        for index, strategy in enumerate(self.distribution):
            if strategy > 0: result.append(index)
        return result

    def get_bases(self):
        # u,v are always basic; offset +1 to support indices
        basic_variables = [0] + [i+1 for i in self.support]

        # number of basic variables will be n+1 for player 1 and m+1 for player 2
        total_basic_variables = self.opponent_number_of_pure_strategies + 1

        # how many variables need to be added to form a basis
        to_add = total_basic_variables - len(basic_variables)

        # find all possible variables to add to a basis
        candidates_to_add = [item for item in range(1, m+n+1) if item not in basic_variables]

        # all subsets from 'candidates' of size 'to_add'
        subsets = list(itertools.combinations(candidates_to_add, to_add))

        all_bases = []
        for indices_to_add in subsets:
            all_bases.append(Basis(sorted(basic_variables + list(indices_to_add)), self))

        lexico_feasible_bases = [basis for basis in all_bases if basis.is_lexico_feasible()]

        return lexico_feasible_bases

class Basis:
    def __init__(self, indices, strategy):
        self.indices = indices
        self.strategy = strategy
        self.player = self.strategy.player
        self.tableau = D if self.player == 1 else C
        self.number_of_pure_strategies = strategy.number_of_pure_strategies
        self.inverse = self.get_inverse()

    def get_inverse(self):
        matrix = self.tableau[:, self.indices]
        if is_singular(matrix):
            return None
        else:
            return inv(matrix)

    def is_lexico_feasible(self):
        # if self.indices == [0,1,2] and self.player == 2:
            # print "here!!!"
            # pdb.set_trace()
        if self.infeasible(): return False
        else: return self.is_lexico_positive()

    def infeasible(self):
        if self.inverse == None:
            return True

        basic_variables_vector = [row[0] for row in self.inverse]
        if min(basic_variables_vector) < 0: return True

        x = self.number_of_pure_strategies
        for i, item in enumerate(self.get_basic_solution()[1:x]):
            if round(item,4) != round(float(self.strategy.distribution[i]),4):
                return True

        return False

    def get_basic_solution(self):
        basic_variables_vector = [row[0] for row in self.inverse]
        result = []
        j = 0
        for i in range(m+n+1):
            if i in self.indices:
                result.append(round(basic_variables_vector[j],4))
                j = j+1
            else:
                result.append(0)
        return result


    def is_lexico_positive(self):
        flag = True
        k = self.inverse.shape[0]
        for i in range(k):
            if flag == False: break
            for j in range(k):
                if self.inverse[i][j] == 0:
                    continue
                elif self.inverse[i][j] < 0:
                    flag = False
                    break
                else:
                    break
        return flag

    def basic_startegy_variables(self):
        result = []
        for i in range(1, self.number_of_pure_strategies + 1):
            if i in self.indices: result.append(i-1)
        return result

class PairOfLexicoFeasibleBases:
    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        self.fulfils_complementarity = self.get_fulfils_complementarity()

    def get_fulfils_complementarity(self):

        flag = True
        basic_solution_x = self.alpha.get_basic_solution()
        basic_solution_y = self.beta.get_basic_solution()

        for i in range(1, m+1):
            if i in self.alpha.indices and i+n in self.beta.indices:
                flag = False

        for i in range(1, n+1):
            if i in self.beta.indices and i+m in self.alpha.indices:
                flag = False
        return flag

    def restricted_matrix(self, matrix):
        alpha_indices = self.alpha.basic_startegy_variables()
        beta_indices = self.beta.basic_startegy_variables()
        temp = matrix[alpha_indices,:]
        result = temp[:,beta_indices]
        return result

    def sign(self):
        t = len(self.alpha.basic_startegy_variables())

        sign_of_A = sign_of_matrix(self.restricted_matrix(A).transpose())
        sign_of_B = sign_of_matrix(self.restricted_matrix(B))

        # print "A transpose"
        # print self.restricted_matrix(A).transpose()
        # print "signA", sign_of_A
        # print
        # print "B"
        # print self.restricted_matrix(B)
        # print "signB", sign_of_B



        return (-1)**(t+1) * sign_of_A * sign_of_B

def is_singular(m): return not is_square(m) or not is_full_rank(m)

def is_square(m): return m.shape[0] == m.shape[1]

def is_full_rank(m): return matrix_rank(m) == m.shape[0]

def sign_of_matrix(matrix):
    if not is_square(matrix):
        return 0
    shape = matrix.shape[0]
    sign = slogdet(matrix)[0] # get the sign of the determinant of 'matrix'
    i = 0
    while sign == 0 and i < shape:
        sign = (-1) * slogdet(replace_column_by_1(matrix, i))[0]
        i = i+1

    return sign

def replace_column_by_1(matrix, index):
    clone = copy(matrix)
    clone[:, index] = 1 # replace column 'index' by the vector 1.
    return clone

def find_eq_by_numbers(number1, number2):
    result = None
    for i in range(len(all_equilibria)):
        current_eq = all_equilibria[i]
        if current_eq.x.number == number1 and current_eq.y.number == number2:
            result = current_eq
    return result

def create_equilibrium_components(component_indices):
    result = []
    for i in range(1, num_of_eq_components + 1):
        component = []
        for pair in component_indices[i]:
            component.append(find_eq_by_numbers(pair[0], pair[1]))
        result.append(EquilibriumComponent(component))
    return result

def create_all_equilibria(equilibria_hash):
    result = []
    for eq in equilibria_hash:

        strategy1 = Strategy(1, [Fraction(x) for x in eq[0]['distribution']], eq[0]['payoff'], eq[0]['number'])
        strategy2 = Strategy(2, [Fraction(x) for x in eq[1]['distribution']], eq[1]['payoff'], eq[1]['number'])
        result.append(Equilibrium(strategy1, strategy2))
    return result

def parse_lrsnash_input():
    with open('lrsnash_input') as f:
        lines = [line.split() for line in f.readlines()]

    m,n = (int(lines[0][0]),int(lines[0][1]))

    A, i = zeros((m,n)), 2
    for j in range(m):
        A[j] = lines[i]
        i+= 1
    i+=1

    B = zeros((m,n))
    for j in range(m):
        B[j] = lines[i]
        i+= 1

    C = create_tableau(A, m+1, 1+n+m)
    D = create_tableau(B.T, n+1, 1+m+n)

    return m,n,A,B,C,D

def create_tableau(matrix, rows, columns):
    result = zeros((rows,columns))
    result[0,:] = [0] + [1 for i in range(columns - rows)] + [0 for i in range(rows-1)]
    for i in range(1,rows):
        zero_row = zeros(rows-1)
        zero_row[i-1] = 1
        result[i,:] = [-1] + matrix[i-1].tolist() + zero_row.tolist()
    return  result

def create_components_dictionary(raw_clique_output):
    raw_clique_output = [item.split() for item in raw_clique_output if item != '\n']
    counter = 0
    result = {}
    for j in range (len(raw_clique_output)):
        if raw_clique_output[j][0] == "Connected":
            counter += 1
            result[counter] = []
            j += 1
            while(j < len(raw_clique_output) and raw_clique_output[j][0] != "Connected"):
                if raw_clique_output[j]:
                    result[counter].append(raw_clique_output[j])
                j+=1
    return counter, result

def create_component(rows):
    result = []
    for row in rows:
        list = (" ".join(row)).split('x')
        if len(list) > 2: print "ERROR!! unexpected format"
        player1_strategies = list[0].replace('{','').replace('}','').split(',')
        player2_strategies = list[1].replace('{','').replace('}','').split(',')
        for strg_player1 in player1_strategies:
            for strg_player2 in player2_strategies:
                pair = [int(strg_player1),int(strg_player2)]
                if pair not in result:
                    result.append(pair)
    return result

def initialize():
    global m, n, A, B, C, D
    global all_equilibria, equilibrium_components, num_of_eq_components, components

    m, n, A, B, C, D  = parse_lrsnash_input()

    with open('index_input', 'r') as file:
        equilibria_hash = json.loads(file.read())
        all_equilibria = create_all_equilibria(equilibria_hash)

    # REFACTOR THIS CRAP!!!!
    with open('clique_output', 'r') as file:
        num_of_eq_components, components_dict = create_components_dictionary(file.readlines())

    component_indices = {}
    for j in range(1, num_of_eq_components + 1):
        component_indices[j] = create_component(components_dict[j])

    components = create_equilibrium_components(component_indices)

def main():

    # eq = all_equilibria[0]
    # for basis in eq.x.lexico_feasible_bases():
    #     print basis.indices

    # print

    # for basis in eq.y.lexico_feasible_bases():
    #     print basis.indices
    #     print basis.inverse

    # print C
    # print


    # pdb.set_trace()

    total = 0
    for component in components:
        for eq in component.extreme_equilibria:
            print "NE", ['%s' % s for s in eq.x.distribution], ['%s' % s for s in eq.y.distribution]
            print "lex-index", eq.lex_index
            print "&&&&&&&&&"

        index  = component.index()
        print "INDEX", index
        total += index
        print "%%%%%%%%%%%%%%%%%%%%%"
    if total != 1:
        print "!!!!!!!!!!!!!!!!!!!!!!"
        print "ERROR!! sum of all indices is not 1"
        print "!!!!!!!!!!!!!!!!!!!!!!"
    return

if __name__ == "__main__":
    initialize()
    main()
