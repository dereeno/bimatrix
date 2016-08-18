import os
#get input

#create 'lrsnash_input' file
# def main():
# execfile('input_genertor.py')
#run lrs_nash
def run_algo():
    os.system('./lrsnash lrsnash_input > lrsnash_output')
    #create 'lrsnash_output' file
    #process output (read 'lrsnash_output') and create 'index_input' file
    execfile('process_lrsnash_output.py')
    #run clique
    os.system('./clique < clique_input > clique_output')

    # run index algorithm
    execfile('index.py')

# if __name__ == "__main__": main()

