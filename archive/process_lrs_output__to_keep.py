import os
from fractions import Fraction
import sys

# original = sys.stdout
# sys.stdout = open("index_input", "w")

execfile('pretty_print.py')
file = 'lrsnash_output'

f= open(file, 'r')
x={}
i=1
for line in f.readlines():
    x[i] = line.split()
    i+=1

######################################################
# Number of extreme equilibria
######################################################
#print x[i-6]
numberOfEq = int(x[i-7][4])
number_of_equilibria = int(x[i-7][4])

# store mixed strategies as arrays of string probabilities
e1 = {}
e2 = {}

# store payoffs
p1 = {}
p2 = {}

######################################################
# DICTIONARIES for mixed strategies
######################################################
# Mixed strategies strings as keys
# strings like '1/2,1/4,1/4'
# Indices as values

dict1 = {}
dict2 = {}

# store indices for mixed strategies for input to clique algorithm
index1 = {}
index2 = {}

# next index for input to clique algorithm
c1 = 1
c2 = 1

eq = -1 # array index of current equilibrium
# (shared by e1,e2,p1,p2,index1,index2)

count = 0 # how many equilibria of II to match with one

for j in range(2,len(x)-7):
    if not x[j]:
        count = 0 # reset count, ready for next set of II's strategies
        continue
    elif x[j][0] == "2":
        processII = True
        count += 1 # one more of II's strategies to pair with I's
        eq += 1
    elif x[j][0] == "1":
        processII = False

    l = len(x[j])
    ##########################################
    # Player II
    ##########################################
    if processII : # loop through all mixed strategies of II
        e2[eq] = x[j][1:l-1]
        p1[eq] = x[j][l-1] # payoffs swapped in lrs output

        e2string = ','.join(e2[eq])

        if e2string not in dict2.keys():
            dict2[e2string] = c2
            c2 += 1
        index2[eq] = dict2[e2string]
    else:
        #################################################
        # Player I
        #################################################
        # Now match all these count-many strategies of II
        # with # subsequent strategy of I

        e1[eq] = x[j][1:l-1]
        p2[eq] = x[j][l-1] # payoffs swapped in lrs output

        e1string = ','.join(e1[eq])

        if e1string not in dict1.values():
            dict1[e1string] = c1
            c1 += 1
        index1[eq] = dict1[e1string]

        for i in range(1,count):
            e1[eq-i] = e1[eq]
            p2[eq-i] = p2[eq]
            index1[eq-i] = index1[eq]

rat = [] # 2d string array with rationals for pretty printing
dec = [] # 2d string array with decimals  for pretty printing
result = []

for i in range(numberOfEq):
    # convert probability strings to fractions to floats to strings
    e1decstr = [str(float(Fraction(s))) for s in e1[i]]
    e2decstr = [str(float(Fraction(s))) for s in e2[i]]
    # initialize empty rows
    rat.append([])
    dec.append([])
    #
    rat[i].append("EE")
    dec[i].append("EE")
    # EE index
    rat[i].append(str(i+1))
    dec[i].append(str(i+1))
    #
    rat[i].append("P1:")
    dec[i].append("P1:")
    # PI strategy index (for connected components)
    rat[i].append("("+str(index1[i])+")")
    dec[i].append("("+str(index1[i])+")")

    result.append([{},{}])

    result[i][0]['number'] = index1[i]


    # PI strategy probabilities
    for entry in e1[i]:
        rat[i].append(entry)
    for entry in e1decstr:
        dec[i].append(entry)

    result[i][0]['distribution'] = e1[i]

    rat[i].append("EP=")
    dec[i].append("EP=")
    # PI payoff
    rat[i].append(str(p1[i]))
    dec[i].append(str(float(Fraction(str(p1[i])))))

    result[i][0]['payoff'] = p1[i]

    #
    rat[i].append("P2:")
    dec[i].append("P2:")
    # PII strategy index (for connected components)
    rat[i].append("("+str(index2[i])+")")
    dec[i].append("("+str(index2[i])+")")

    result[i][1]['number'] = index2[i]
    # PII strategy probabilities
    for entry in e2[i]:
        rat[i].append(entry)
    for entry in e2decstr:
        dec[i].append(entry)

    result[i][1]['distribution'] = e2[i]

    rat[i].append("EP=")
    dec[i].append("EP=")
    # PII payoff
    rat[i].append(str(p2[i]))
    dec[i].append(str(float(Fraction(str(p2[i])))))
    result[i][1]['payoff'] = p2[i]

print numberOfEq
# pretty_print(rat)
pretty_print(dec)
print
print
print "---------------------"

print result

# #############################################################
# # CLIQUE ENUMERATION
# #############################################################
# open clique enumeration input file
fcin = open('clique_input', 'w')
# print indices to clique enumeration input file
for i in range(numberOfEq):
    fcin.write("{0} {1}\n".format(index1[i],index2[i]))
# close file
fcin.close()
# do clique enumeration
os.system("./clique < clique_input > clique_output")
# open clique enumeration output file
fcout = open('clique_output', 'r')
# print contents
print(fcout.read())
fcout.close()
#   sys.stdout = original

