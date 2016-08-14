import string

# requires input to really be a matrix (dimension 2), not just a list
def pretty_print (my_matrix):

    # list of max lengths in each column
    max_lens = [max([len(str(r[i])) for r in my_matrix])
                            for i in range(len(my_matrix[0]))]

    print "\n".join(["".join([string.rjust(str(e), l + 2)
                        for e, l in zip(r, max_lens)]) for r in my_matrix])
