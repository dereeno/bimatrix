#!/usr/bin/python
from numpy.linalg import inv as inverse, slogdet as determinant_sign, matrix_rank
from itertools import combinations as all_subsets
from index_initialise import *
from fractions import Fraction


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
        self.lexico_feasible_bases = self.get_lexico_feasible_bases()

    def get_support(self):
        result = []
        for index, strategy in enumerate(self.distribution):
            if strategy > 0:
                result.append(index)
        return result

    def get_lexico_feasible_bases(self):
        # u/v are always basic; offset +1 to support indices
        basic_variables = [0] + [i+1 for i in self.support]

        # 'basis_size' will be n+1 for player 1 and m+1 for player 2
        basis_size = self.opponent_number_of_pure_strategies + 1

        # 'how_many_to_add' gets the number of variables we need to add to form a basis
        how_many_to_add = basis_size - len(basic_variables)

        # 'candidates_to_add' gets all possible variables we can add to a basis
        candidates_to_add = \
            [item for item in range(1, m+n+1) if item not in basic_variables]

        # 'subsets' gets all subsets of 'candidates_to_add' of size 'how_many_to_add'
        subsets = all_subsets(candidates_to_add, how_many_to_add)

        all_bases = []
        for indices_to_add in subsets:
            indices = sorted(basic_variables + list(indices_to_add))
            all_bases.append(Basis(indices, self))

        lexico_feasible_bases = \
            [basis for basis in all_bases if basis.is_lexico_feasible()]

        return lexico_feasible_bases

class Basis:
    def __init__(self, indices, strategy):
        self.indices = indices
        self.strategy = strategy
        self.player = self.strategy.player
        self.number_of_pure_strategies = strategy.number_of_pure_strategies
        self.matrix = matrix_1 if self.player == 1 else matrix_2
        self.basic_matrix_inverse = self.get_basic_matrix_inverse()

    def get_basic_matrix_inverse(self):
        basic_matrix = self.matrix[:, self.indices]
        if Basis.is_singular(basic_matrix):
            return None
        else:
            return inverse(basic_matrix)

    def is_lexico_feasible(self):
        if self.not_a_basis():
            return False
        elif self.infeasible():
            return False
        elif self.solution_does_not_correspond_to_strategy():
            return False
        else:
            return self.is_lexico_positive()

    def not_a_basis(self):
        return self.basic_matrix_inverse == None

    def infeasible(self):
        return min(self.basic_variables_vector()) < 0

    def solution_does_not_correspond_to_strategy(self):
        strategy_variables = self.basic_solution()[1:self.number_of_pure_strategies+1]
        for i, item in enumerate(strategy_variables):
            # checking whether strategy distribution is equal to basic solution
            if item != round(float(self.strategy.distribution[i]), 5):
                return True

        return False

    def is_lexico_positive(self):
        flag = True
        dimension = self.basic_matrix_inverse.shape[0]
        for row in range(dimension):
            if flag == False:
                break
            for column in range(dimension):
                current = round(self.basic_matrix_inverse[row][column], 5)
                if current == 0:
                    continue
                elif current < 0:
                    flag = False
                    break
                else:
                    break
        return flag

    def basic_variables_vector(self):
        # basic variables vector will be the first column of the basic inverse matrix
        return [round(row[0],5) for row in self.basic_matrix_inverse]

    def basic_solution(self):
        basic_variables_vector = self.basic_variables_vector()
        result = []
        j = 0
        # m+n+1 is the number of components in the variable vector (number of columns)
        for i in range(m+n+1):
            if i in self.indices:
                result.append(basic_variables_vector[j])
                j = j+1
            else:
                result.append(0)

        return result

    def basic_startegy_variables(self):
        result = []
        for i in range(1, self.number_of_pure_strategies + 1):
            if i in self.indices: result.append(i-1)
        return result

    @staticmethod
    def is_singular(matrix):
        return not Basis.is_square(matrix) or not Basis.is_full_rank(matrix)

    @staticmethod
    def is_square(matrix):
        return matrix.shape[0] == matrix.shape[1]

    @staticmethod
    def is_full_rank(matrix):
        return matrix_rank(matrix) == matrix.shape[0]

class PairOfLexicoFeasibleBases:
    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        self.fulfils_complementarity = self.get_fulfils_complementarity()

    def get_fulfils_complementarity(self):
        flag = True

        for i in range(1, m+1):
            if i in self.alpha.indices and i+n in self.beta.indices:
                flag = False
                break

        if flag:
            for i in range(1, n+1):
                if i in self.beta.indices and i+m in self.alpha.indices:
                    flag = False
                    break

        return flag

    def square_submatrix(self, matrix):
        alpha_indices = self.alpha.basic_startegy_variables()
        beta_indices = self.beta.basic_startegy_variables()
        return matrix[alpha_indices,:][:,beta_indices]

    def sign(self):
        t = len(self.alpha.basic_startegy_variables())

        sign_of_A = sign_of_matrix(self.square_submatrix(A).transpose())
        sign_of_B = sign_of_matrix(self.square_submatrix(B))

        return (-1)**(t+1) * sign_of_A * sign_of_B

def sign_of_matrix(matrix):
    dimension = matrix.shape[0]
    sign = determinant_sign(matrix)[0] # get the sign of the determinant of 'matrix'
    i = 0

    while sign == 0 and i < dimension:
        sign = (-1) * determinant_sign(replace_column_by_1(matrix, i))[0]
        i = i+1

    return sign

def replace_column_by_1(matrix, index):
    clone = copy(matrix)
    clone[:, index] = 1 # replace column 'index' by the vector 1.
    return clone

def create_all_equilibria(equilibria_hash):
    result = []
    for eq in equilibria_hash:
        distribution1 = [Fraction(x) for x in eq[0]['distribution']]
        distribution2 = [Fraction(x) for x in eq[1]['distribution']]
        payoff1, number1 = eq[0]['payoff'], eq[0]['number']
        payoff2, number2 = eq[1]['payoff'], eq[1]['number']
        strategy1 = find_or_create_strategy(1, distribution1, payoff1, number1)
        strategy2 = find_or_create_strategy(2, distribution2, payoff2, number2)
        result.append(Equilibrium(strategy1, strategy2))
    return result

def find_or_create_strategy(player, distribution, payoff, number):
    strategy_hash = strategy_hash_player_1 if player == 1 else strategy_hash_player_2
    if number in strategy_hash.keys():
        return strategy_hash[number]
    else:
        strategy = Strategy(player, distribution, payoff, number)
        strategy_hash[number] = strategy
        return strategy

def create_equilibrium_components(all_equilibria):
    result = []
    for i in range(len(components_hash)):
        component = []
        for pair in components_hash[i]:
            component.append(find_eq_by_numbers(pair[0], pair[1], all_equilibria))
        result.append(EquilibriumComponent(component))
    return result

def main():
    all_equilibria = create_all_equilibria(equilibria_hash)
    components = create_equilibrium_components(all_equilibria)

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

if __name__ == "__main__": main()
