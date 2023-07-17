# Checkers!

A simple 2-player game of checkers (AKA draughts). Created using Python (v 3.11.3) and Pygame library (v. 2.5.0).

![checkers_readme_1](https://github.com/shikimin/checkers/assets/104809403/c84c4a33-e430-42e3-98ea-9d4e2c9c65d0)&emsp;&emsp;![checkers_readme_2](https://github.com/shikimin/checkers/assets/104809403/75127e72-3143-4c10-8eed-a75ad340fa17)


## Getting Started

1. Download the files in this repository as a ZIP file (via the green `<> Code` on the top right) or run `git clone https://github.com/shikimin/checkers.git` into a terminal if you have git installed.
2. Install the Pygame library with the command `pip install pygame`.
3. Run main.py.

## Rules

This game assumes that you already know the general rules of checkers (i.e. pieces can only move diagonally on dark pieces, opponent pieces can be captured by jumping over them, players can't take two turns in a row**, etc). Pieces can be moved by clicking the desired piece and then clicking the desired destination square. Selected pieces will be highlighted in yellow. Pieces will not move if the destination squares are not reached with valid moves. 

This version of checkers uses triple kings in addition to the standard king. 

Kings get promoted from regular pieces after they reach the end of the opponent's side. Kings have the same abilities as regular pieces but can also move backwards. They can also move to any square along a diagonal as long as the diagonal contains only one opponent piece and the king is moving to capture it. 

A triple king gets promoted from a king after they return from the end of opponent's side to the end of their home side. Triple kings have the same abilities as regular kings but can jump over and capture two opponent pieces that are right next to each other. They can also jump over a piece of the same color to traverse the board faster.

** To perform a double/triple/quadruple jump, you will have to move your piece to each empty square.
