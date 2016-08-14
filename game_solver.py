import os
#get input

#create 'lrsnash_input' file
# execfile('input_genertor.py')
#run lrs_nash
os.system('./lrsnash lrsnash_input > lrsnash_output')
#create 'lrsnash_output' file

#process output (read 'lrsnash_output') and create 'index_input' file
execfile('process_lrsnash_output.py')
#run clique
os.system('./clique < clique_input > clique_output')

# run index algorithm
execfile('index.py')