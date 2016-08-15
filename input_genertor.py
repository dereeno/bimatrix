import random

# m = random.randrange(2, 4)
# n = random.randrange(2, 4)

m=7
n=8

with open('lrsnash_input', 'w') as file:
    file.write("{0} {1}\n".format(m,n))
    file.write('\n')

    for i in range(m):
        for j in range(n):
            file.write("{0} ".format(random.randrange(1,10)))
        file.write('\n')

    file.write('\n')

    for i in range(m):
        for j in range(n):
            file.write("{0} ".format(random.randrange(1,10)))
        file.write('\n')

