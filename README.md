# 2048---AI
    This project is an implementation of the classic **2048 game** with:
    A playable version
    An **AI player** that uses heuristics to choose movements
    Basic animations, colors, and game-over screen with restart/quit options

---

## Features
    Manual play (arrow keys)
    AI play (heuristic evaluation)
    Animations for tile movement

---

## Project Structure

    - main.py               # Entry point, runs the game
    - src/
        - game.py           # Game logic & board state
        - tile.py           # Tile rendering and animations
        - HeuristicsAI.py   # AI player (heuristics based)
    - requirements.txt      # Dependancies
    README.md               # Project documentation

## Controls
    **Arrow keys** in manual mode

---

## AI
    The AI currently uses a **heuristics evaluation function**
    **Monotonicity** prefers boards where the tiles increase in one direction
    **Empty cels** rewards having more open space
    **Max tile in corner** encourages keeping the biggest tile in a corner

    The AI tries all possible moves, simulates them, and picks the best one.

---

## Instalation

```bash
git clone https://github.com/BobySandala/2048---AI.git
cd 2048---AI
python -m venv venv
source venv/bin/activate # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## Run
```bash
python main.py
```

