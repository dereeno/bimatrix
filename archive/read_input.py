from numpy import zeros
import json

def parse_lrsnash_input(filename):
	with open(filename) as f:
		lines = f.readlines()

	m,n = (int(lines[0].split()[0]),int(lines[0].split()[1]))

	A, i = zeros((m,n)), 2
	for j in range(m):
		A[j] = lines[i].split()
		i+= 1
	i+=1

	B = zeros((m,n))
	for j in range(m):
		B[j] = lines[i].split()
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

def create_dictionary(file_reader):
	result = {}
	i=1
	for line in file_reader.readlines():
		result[i] = line.split()
		i += 1
	file_reader.close()
	return result

def parse_equilibrium(unparsed_equilibrium, num_of_strategies):
	number = int(unparsed_equilibrium[0].replace('(','').replace(')',''))
	distribution = []
	for i in range(num_of_strategies):
		distribution.append(float(unparsed_equilibrium[i+1]))
	payoff = unparsed_equilibrium[-1]
	return distribution, payoff, number

def create_extreme_equilibria(number_of_extreme_equilibria, dictionary,m,n):
	result = []
	offset = 2
	for k in range(number_of_extreme_equilibria):
		equilibrium_string = " ".join(dictionary[k + offset])
		equilibrium_array = equilibrium_string.split("P1:")[1].split("P2:")
		dist_x, payoff_x, number_x = parse_equilibrium(equilibrium_array[0].split(),m)
		dist_y, payoff_y, number_y = parse_equilibrium(equilibrium_array[1].split(),n)
		result.append([[1, dist_x, payoff_x, number_x], [2, dist_y, payoff_y, number_y]])
	return result

def create_components_dictionary(number_of_extreme_equilibria, dictionary):
	number_of_components = 0
	result = {}
	i = number_of_extreme_equilibria + 3	# offset by 3
	for j in range (i, len(dictionary)):
		if dictionary[j] and dictionary[j][0] == "Connected":
			number_of_components += 1
			result[number_of_components] = []
			j += 1
			while(dictionary[j] and dictionary[j][0] != "Connected"):
				if dictionary[j]: result[number_of_components].append(dictionary[j])
				j+=1
	return number_of_components, result

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

def get_variables_from_input_parser():
    global m,n, dictionary, number_of_extreme_equilibria, number_of_components
    m, n, A, B, C, D = parse_lrsnash_input('lrsnash_input')
    dictionary = create_dictionary(open('index_input', 'r'))
    number_of_extreme_equilibria = int(dictionary[1][0])
    extreme_equilibria_raw = create_extreme_equilibria(number_of_extreme_equilibria, dictionary,m,n)
    number_of_components, components_dict = create_components_dictionary(number_of_extreme_equilibria, dictionary)
    component_indices = {}
    for j in range(1, number_of_components + 1):
        component_indices[j] = create_component(components_dict[j])

    return m,n,A,B,C,D, number_of_extreme_equilibria, extreme_equilibria_raw, number_of_components, component_indices

















