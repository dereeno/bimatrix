Installation and usage instructions.

Folder structure and key files:

bimatrix/
    requirements.txt
    app.py
    game_solver.py
    index_algorithm.py

    clique/
        clique

    lrs/
        lrs_input
        lrsnash
        process_lrsnash_output.py

    coffee/
        all.coffee

    sass/
        all.sass

    templates/
        index.html

Description of the different keys files:
    - requirements.txt; list of software dependencies to install in order to run the web server.
    - app.py; contains the code for the web server (Flask Python application).
    - game_solver.py; Python script that executes the game solving algorithm.
    - index_algorithm.py; contains the core of the index computation algorithm.
    - lrs/lrsnash; executable file for the lrsnash program implemented by David Avis.
    - clique/clique; executable file for a clique enumeration program implemented by Bernhard von Stengel.
    - lrs/lrs_input; main input file of the program (contains matrix dimensions and two payoff matrices)
    - lrs/process_lrsnash_output.py; Python code written by Raul Savani that parses the output of 'lrsnash' and creates the input to 'clique'.
    - coffee/all.coffee; JavaScript file for the web page (written in CoffeeScript).
    - sass/all.sass; CSS (styling) for web page (written in SASS)
    - templates/index.html; HTML for the web page.

This program can run in two ways:
    1. Through the command line.
    2. Through a web browser using web interface.

In order to run through the command line one should create a file named 'lrsnash_input', place it in the 'lrs' directory and execute the following command:

    python game_solver.py

The structure of the 'lrsnash_input' should be as follows.
first line contains the matrix dimensions separated by space.
blank line.
payoff matrix to player 1 separated by spaces.
blank line.
payoff matrix to player 2 separated by spaces.

Example for an lrsnash_input file for  2 x 3 bimatrix game:

2 3

1 2 3
4 5 6

7 8 9
10 11 12

Output will be printed to the console.
Output example for the above game:

INPUT:
Payoff matrix to player 1:
[[ 1.  2.  3.]
 [ 4.  5.  6.]]
Payoff matrix to player 2:
[[  7.   8.   9.]
 [ 10.  11.  12.]]

OUTPUT:
EXTREME EQUILIBRIA
   Equilibrium number: 1
     Player 1
       Strategy number: x1
       Distribution: ['0', '1']
       Payoff: 6
     Player 2
       Strategy number: y1
       Distribution: ['0', '0', '1']
       Payoff: 12

EQUILIBRIUM COMPONENTS
   Component number: 1
     Nash subsets:
       ['x1'] X ['y1']
     Extreme Equilibria
       Number: 1 , Lex-index: 1.0


The second option is to run the web server and operate the program using the web browser.
A live running version of the program is available at: https:/bimatrix.herokuapp.com
In order to run the server we need to install all its components using the following command (run from root directory of the project; requires up to date version of Python to be already installed).

    pip install -r requirements.txt

Next we can run the local server using the following command:

    python app.py

Then we can access the application with the following local url.

    http://localhost:5000/
