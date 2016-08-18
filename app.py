# imports
from flask import Flask, render_template, request, jsonify
import json
import pdb
import game_solver

# initilize flask
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':

        write_input_file(request.form)
        game_solver.run()

        with open('index_output', 'r') as file:
            data = json.loads(file.read())

        return jsonify(data)
    return render_template('index.html')


def write_input_file(form):
    matrix_a, matrix_b = form['A'], form['B']
    m, n = form['m'], form['n']
    with open('lrsnash_input', 'w') as file:
        file.write(m + ' ' + n + '\n\n')
        for row in json.loads(matrix_a):
            for item in row:
                file.write(item + " ")
            file.write('\n')

        file.write('\n')

        for row in json.loads(matrix_b):
            for item in row:
                file.write(item + " ")
            file.write('\n')


# run the server
if __name__ == '__main__':
    app.run(debug=True)

# boom!