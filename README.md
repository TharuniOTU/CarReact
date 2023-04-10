# CarReact

### Problem
How can we simulate car collision detection and response? <br>
How does autonmous vehicles compare with manual?

### Approach
Completed using Pygame on Visual Studio Code. Loaded images of a: background, car sprites, and a box. 
The position of the car and the background is fixed while random sampling was used for the location of the box.
Car's state is updated using Big 5 equations, and rigid body collision theory is used when the object and car come into contact.
Chi-Square test in pytest is used to compare the actual data for random positions of the box as well as the breaking distance of the car
to measure accuracy.

### Running the Code
Make sure you have python3 installed along with the necessary libraries (ex. pygame, pytest, matplotlib) <br>
On terminal run python3 main.py <br>
To run pytest run the command python3 -m pytest -s --cov

### Contributors 
Tharuni Iranjan
