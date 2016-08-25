import os
import index_algorithm
import sys

sys.path.append(os.getcwd())

def run():
    #running lrsnash
    if not os.path.isfile('lrs/lrsnash'): #ugly hack to make heroku compile lrsnash
        compile('lrsnash')
    os.system('./lrs/lrsnash lrs/lrsnash_input > lrs/lrsnash_output')
    execfile('lrs/process_lrsnash_output.py')

    #running clique
    if not os.path.isfile('clique/clique'): #ugly hack to make heroku compile clique
        compile('clique')
    os.system('./clique/clique < clique/clique_input > clique/clique_output')

    #running index calculation
    index_algorithm.run()

def compile(filename):
    if filename == 'lrsnash':
        os.system('gcc -O3 -o lrs/lrsnash lrs/lrsnash.c lrs/lrsnashlib.c lrs/lrslib.c lrs/lrsmp.c')
    elif filename == 'clique':
        os.system('gcc -O3 -o clique/clique  clique/coclique3.c')


if __name__ == '__main__':
    run()
