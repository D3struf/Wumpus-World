# Wumpus-World
A Wumpus World Game with Logical Agent Solver


## Table of Contents

- [Wumpus-World](#wumpus-world)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Game Rules](#game-rules)
  - [Agent Demo](#agent-demo)
  - [Screenshots](#screenshots)

## Introduction

The Wumpus World Game is a text-based adventure game where the player explores a cave inhabited by dangerous creatures such as wumpuses and pits. The goal of the game is to navigate through the cave, collect treasures, and avoid hazards to reach the exit safely.

This project provides an implementation of Wumpus World where a player can play and also let AI play the game. The AI uses the propositional logic as a knowledge base and provide a challenging gameplay experience.

## Features

- Navigate through a grid-based cave environment.
- Encounter wumpuses, pits, gold, and other obstacles.
- Use a dagger to defend against wumpuses.
- Collect gold and reach the exit to win the game.
- Customizable game modes (AI or Player).

## Installation

To run the game, follow these steps:

1. Clone the repository to your local machine:

    ``` bash
    git clone https://github.com/your-username/wumpus-world-game.git
    ```

2. Navigate to the project directory:

    ``` bash
    cd Wumpus-World
    ```

3. Install the required dependencies:

    ``` bash
    pip install -r requirements.txt
    ```

## Usage

To start the game, run the following command:

``` bash
python main.py
```

Follow the on-screen instructions to play the game. Input your moves using the command-line interface and enjoy the gameplay experience!

## Game Rules

- *Objective*: The objective of the game is to navigate through the cave, collect gold, and reach the exit safely.
- *Hazards*: The cave is filled with dangers such as wumpuses and bottomless pits. If the player encounters a wumpus, they will be eaten and lose the game. Falling into a pit also results in instant death.
- *Weapons*: Players can find a dagger in the cave, which can be used to defend against wumpuses. If the player has a dagger and encounters a wumpus, they can choose to fight or flee.
- *Gold*: Scattered throughout the cave are gold coins.
- *Exit*: The exit is located at the starting position in the cave. Once the player has collected enough gold, they can head to the exit to escape and win the game.

For more detailed rules, refer to [Wumpus World Rules](https://www.javatpoint.com/the-wumpus-world-in-artificial-intelligence).

## Agent Demo
https://github.com/D3struf/Wumpus-World/assets/93712294/b62071dc-a9d1-4aef-8e2d-828dde02df37

## Screenshots

- Home Page
  ![Home Page](https://github.com/D3struf/Wumpus-World/assets/93712294/1db5bd4f-9d1c-410e-a672-9fe879352e45)

- Instruction Pages
  ![Instruction Page 1](https://github.com/D3struf/Wumpus-World/assets/93712294/cb3a884f-c113-4f2e-8deb-27563454f66c)
  ![Instruction Page 2](https://github.com/D3struf/Wumpus-World/assets/93712294/967ab3ab-e584-4c5d-8492-d5d25f12f5e2)

- Mode Selection
  ![image](https://github.com/D3struf/Wumpus-World/assets/93712294/70023f00-6177-4813-b8e3-92634228f439)

- Player Mode Game
  ![image](https://github.com/D3struf/Wumpus-World/assets/93712294/3e37316c-9019-4d31-926e-de2819714ace)

- AI Mode Game
  ![image](https://github.com/D3struf/Wumpus-World/assets/93712294/013ce10d-f137-44fe-ae42-744bdaa991dc)

- Winner Panel
  ![image](https://github.com/D3struf/Wumpus-World/assets/93712294/53766f71-6638-40c6-a7c4-b0d337716b85)

- Game Over Panel
  ![image](https://github.com/D3struf/Wumpus-World/assets/93712294/937f4c05-e364-49ff-bafa-013df6ade677)


