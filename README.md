# CubeSim
A Rubik's Cube simulator and solver built in Python with Pygame.
![Cover pic](https://raw.githubusercontent.com/V-Wong/CubeSim/master/cover.webp)

## Features ##
* 2d visualisation of Rubik's cube (2 x 2 and 3 x 3)
* Keyboard controls for face turns
* Parsing scramble strings and performing the scrambles on the cube
* Generation of animated solutions based on the LBL beginner's method

## Planned Features ##
* Generalisation up to n x n Rubiks Cubes
* Implementation of more sophisticated and efficient Rubik's cube solving algorithms

## Implementation ##
### Cube ###
This program uses a relatively simplistic representation of the Rubiks Cube. We simply consider the cube to be an array of 6 2-dimensional arrays, each representing a face of the cube. Each element of these 2-dimensional arrays then represents a sticker on the cube.

A single face turn then can be implemented by:

1. Rotating all elements of the given face by 90 degrees
2. Cycling all the rows/columns that intersect with the given face on all adjacent faces

For simplicity, but possibly at the cost of efficiency, all counter-clockwise and double turns are implemented as repeated single face turns.

### Solving ###
The program implements a simplified variant of the LBL beginner's method. This method involves:

1. Solving first layer cross
2. Solving first layer corners
3. Solving middle layer edges
4. Solving top layer edge orientation
5. Solving top layer corner orientation
6. Solving top layer corner permutation
7. Solving top layer edge permutation

For programming simplicity, the program always solves pieces in a fixed order, unlike how a human would solve. Furthermore, the program solves the cube by performing simple setup moves that reduce the pieces into a state that can be solved by a simple algorithm. This creates a simple program at the detriment of movecount efficiency.
