
#! /usr/bin/env python

from fractions import Fraction
import fractions
import numpy as np
import cgi, os
form = cgi.FieldStorage()   # FieldStorage object to
                            # hold the form data

execfile('pretty_print.py')

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers
#print "Content-Type: text/plain;charset=utf-8"
#print # REQUIRED FOR SOME REASON

######################################################
# GET GAME DATA FROM FORM
# Need to check for empty fields, else we get an error
######################################################

maxsize = 15

# Get type
gtype = form["type"].value

# Dimensions
if form.has_key('dim'):
    dim = form["dim"].value
    ###################################################
    # NEED TO CHECK FOR DODGY INPUT
    entries = dim.split()
    try:
    	nrows = int(entries[0]) # USE TRY
    except:
    	print "Bad dimensions, using default 2 rows<br>"
    	nrows = 2
    try:
    	ncols = int(entries[1])
    except:
    	print "Bad dimensions, using default same number of columns as rows<br>"
        ncols = nrows
    if nrows > maxsize:
		nrows = maxsize
		print "<strong>Number of rows capped at ", maxsize, "</strong><br>"
    if ncols > maxsize:
		ncols = maxsize
		print "<strong>Number of cols capped at ", maxsize, "</strong><br>"
    if gtype == "sym" and ncols != nrows:
        	print "Symmetric game but number of columns and rows differ"
        	print "Taking same number of columns as rows"
        	ncols = nrows # allows us to take transpose in this case
    ###################################################
else:
    print "Try again; you did not correctly enter dimensions of the game"

# Matrix 1
if form.has_key('matrix1'):
    input1  = form["matrix1"].value
else:
    input1  = None
    #print "Note: no matrix for player 1, using all zero default"

# Matrix 1
if form.has_key('matrix2'):
    input2  = form["matrix2"].value
else:
    input2  = None
    #print "Note: no matrix for player 2, using all zero default"


######################################################
# FILL MATRIX INPUT
# Start with all zero nrows x ncols matrix
# Replace with valid entries from input
######################################################
def fillMatrix(input,nrows,ncols):
    matrix = np.zeros((nrows,ncols),dtype=fractions.Fraction)
    if input is not None:
        rows = input.splitlines()
        for i in range(min(nrows,len(rows))):
            row = rows[i].split()
            for j in range(min(ncols,len(row))):
                try:
                    matrix[i][j] = Fraction(row[j])
                except:
                    pass
    return(matrix)

matrix1 = fillMatrix(input1,nrows,ncols)

# create matrix2 according to game type gtype
if gtype == 'general':
	matrix2 = fillMatrix(input2,nrows,ncols)
elif gtype == 'sym':
	matrix2 = matrix1.T
else:
	matrix2 = -matrix1


print "<font face=\"helvetica,arial\">";
print "<HR NOSHADE><H1>Solution Page</H1><HR NOSHADE>";
print "Please check that the matrices displayed below are as you intended.  ";
print "If not please go back and re-enter the game.<BR><HR>";
print "</font>";
print "<pre>"

print nrows, "x", ncols, "Payoff matrix A:\n"
#print str(matrix1).replace('[','').replace(']', '')
pretty_print(matrix1)
print "\n\n"
print nrows, "x", ncols, "Payoff matrix B:\n"
#print str(matrix2).replace('[','').replace(']', '')
pretty_print(matrix2)

print

######################################################
# WRITE GAME MATRICES FILE
######################################################
f = open("../bimatrix/games/game", "w")
f.write(str(nrows) + ' ' + str(ncols))
f.write('\n\n')
print >>f, str(matrix1).replace('[','').replace(']', '')
f.write('\n\n')
print >>f, str(matrix2).replace('[','').replace(']', '')
f.close()


######################################################
# RUN setupnash
######################################################
os.system("../bimatrix/setupnash ../bimatrix/games/game ../bimatrix/games/m1 ../bimatrix/games/m2 >/dev/null")
#os.system("../bimatrix/lrslib-042c/nash ../bimatrix/games/m1 ../bimatrix/games/m2 ../bimatrix/games/out >/dev/null")
os.system("nice -n 19 ../bimatrix/nash ../bimatrix/games/m1 ../bimatrix/games/m2 >../bimatrix/games/out")

file = "../bimatrix/games/out"

execfile('process_lrs_output.py')

print "</pre>"
#print "</body>"
#print "</html>"

