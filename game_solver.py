import os
import index

def run():
    if not os.path.isfile('lrsnash'): #ugly hack to make heroku compile lrsnash
        os.system('gcc -O3 -o lrsnash lrsnash.c lrsnashlib.c lrslib.c lrsmp.c')
    os.system('./lrsnash lrsnash_input > lrsnash_output')
    execfile('process_lrsnash_output.py')
    if not os.path.isfile('clique'): #ugly hack to make heroku compile clique
        os.system('gcc -O3 -o clique  coclique3.c')
    os.system('./clique < clique_input > clique_output')
    index.main()

