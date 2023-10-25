# Conway's Game of Life

Implementation of the famous Conway's Game of Life using Python and Pygame
[TODO: gif intro]

## Introduction

[Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) is a classic cellular automaton devised by British mathematician [John Horton Conway](https://en.wikipedia.org/wiki/John_Horton_Conway) in 1970. It's not a conventional game in the traditional sense but a simulation of a simple and fascinating universe of "*cells*" that follow specific rules to evolve over generations. The game demonstrates how complex patterns can emerge from simple rules and is a popular subject in computer science and recreational mathematics.

It is a *zero-player game*, meaning that its evolution is determined by its initial state, requiring no further input. One interacts with the Game of Life by creating an initial configuration and observing how it evolves. It is [Turing complete](https://en.wikipedia.org/wiki/Turing_completeness) and can simulate a universal constructor or any other Turing machine. In other words, anything that can be computed algorithmically can be computed within the *Game of Life*.

## Rules
The universe of the Game of Life is a two-dimensional orthogonal grid of square cells, each of which is in one of two possible states: **living** or **dead**. Every cell interacts with its eight neighbors, which are the cells that are horizontally, vertically, or diagonally adjacent.

At each step in time, the following transitions occur:

- **Underpopulation**: Any living cell with fewer than two living neighbors dies.
- **Survival**: Any live cell with two or three living neighbors lives on to the next generation.
- **Overpopulation**: Any living cell with more than three living neighbors dies.
- **Reproduction**: Any dead cell with exactly three living neighbors becomes a living cell.

All other dead cells stay dead. These simple rules lead to fascinating patterns and behaviors that can be observed as the game progresses.

## Project structure
TODO
TODO: last file is 'seed_patterns.yml'

## Seed patterns
The initial pattern constitutes the seed of the system. The first generation is created by applying the above rules simultaneously to every cell in the seed, live or dead; births and deaths occur simultaneously. Each generation is a pure function of the preceding one. The rules continue to be applied repeatedly to create further generations.
[TODO: add the 9 seed patterns]

## Getting started

## Controls

## Customize your Game
You can customize the game by modifying the initial grid configuration, rules, or visuals.

## About Pygame
[Pygame](https://www.pygame.org/docs/) is a cross-platform set of Python modules designed for writing video games. It is built on top of the *Simple DirectMedia Layer* (SDL) library and provides a simple way to create games and multimedia applications. Pygame is widely used for 2D game development and interactive simulations. In this project, Pygame is used to create a graphical interface for the Conway's Game of Life simulation.

## Contribute
Contributions to this project are welcome! If you'd like to improve the game, fix bugs, or add new features, feel free to fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE file](TODO) for details.

## Acknowledgments
John Horton Conway for inventing Conway's Game of Life.
