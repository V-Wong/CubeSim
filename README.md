# CubeSim
## Overview
A simple Rubik's Cube simulator and solver built in Python with Pygame for visual rendering and controls.

### Features
* Two-dimensional visualisation of a 3x3 Rubik's cube
* Keyboard controls for face turns and rotations.
* Generation of animated solutions based on the layer-by-layer method.

### Picture of Program
<p align="center">
<img src="/cover.webp" width="800">
<p>

## Quick Start
To work on or run this project, start by creating a virtual environment:
```
$ virtualenv venv
```

Activate the virtual environment by running:
```
$ source venv/bin/activate
```

Install the dependencies inside the virtual environment
```
$ pip install -r requirements.txt
```

Launch the main graphical user interface
```
$ python3 -m src.main
```

## Project Structure
### ``src/cube``
This folder contains the majority of the core logic for representing the Cube and the solver.
- ``gui.py`` - The **Gui class** which acts as the interface between the **Cube class** and **Pygame**.
- ``cube.py`` - The **Cube class** which encapsulates all the main logic for representing a Rubik's Cube.
- ``history_cube.py`` - A **subclass of Cube** that has methods to record all moves applied.
- ``solver.py`` - The **solving functions** that generate solutions given an instance of a **Cube**.
- ``move.py`` - A simple **Move dataclass** to encapsulate information about specific moves.
- ``pieces.py`` - Simple **Edge and Corner dataclasses** to encapsulate information about pieces.
- ``colour.py`` - A simple **Colour type definition** to wrap around RGB colour tuples.

### ``src/scramble``
This folder contains any logic regarding scramble generation and scramble parsing.
- ``generator.py`` - A simple **scramble generation function** that randomly selects moves to produce a scramble.
- ``parser.py`` - A set of **parsing functions** to convert between moves of **str** type and **Move** type.

### ``src/stats``
This folder contains a set of statistical analysis functions to analyse the solver.
- ``statistics.py`` - A simple **Statistics class** that generates scrambles and solutions while recording movecounts in a spreadsheet.

### ``tests``
This folders contains the tests which can be run using ``python3 -m pytest``.
- ``test_cube.py`` - A **set of tests** to ensure data invariants for the cube are maintained and to test the **solving functions**.
 
## Implementation ##
### Cube ###
This program uses a relatively simplistic representation of the Rubik's Cube. We simply consider the cube to be an array of 6 2-dimensional arrays, each representing a face of the cube. Each element of these 2-dimensional arrays then represents a sticker on the cube.

A single face turn then can be implemented by:

1. Rotating all elements of the given face by 90 degrees
2. Cycling all the rows/columns that intersect with the given face on all adjacent faces

### Solving ###
The program implements a simplified variant of the LBL beginner's method. This method closely approximates how a normal beginner solver would solve a cube, although without the aid of human intuition. This approach to solving a cube is substantially less move optimal compared to more sophisticated computer-based algorithms, but was chosen due to ease of implementation and relatively low computation cost.
