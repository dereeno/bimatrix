web: gcc -O3 -o lrsnash lrsnash.c lrsnashlib.c lrslib.c lrsmp.c
web: gcc -O3 -o clique  coclique3.c
web: gunicorn app:app
worker: ./lrsnash lrsnash_input > lrsnash_output
worker: ./clique < clique_input > clique_output