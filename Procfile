web: gunicorn app:app
worker: ./lrsnash lrsnash_input > lrsnash_output
worker: ./clique < clique_input > clique_output