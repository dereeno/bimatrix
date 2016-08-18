import os
import index

def run():
    os.system('./lrsnash lrsnash_input > lrsnash_output')
    execfile('process_lrsnash_output.py')
    os.system('./clique < clique_input > clique_output')
    index.main()

# if __name__ == "__main__": run_algo()

