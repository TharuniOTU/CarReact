# CarReact

### Problem
1.	How can we simulate an autonomous vehicle reacting to an object randomly appearing on the road? <br>
2.	How does the response time between a person compare with an autonomous vehicle?


### Approach
Completed using Pygame on Visual Studio Code. Loaded images of a: background, car sprites, and a box. 
The position of the car and the background is fixed while random sampling was used for the location of the box.
Car's state is updated using Big 5 equations, and rigid body collision theory is used when the object and car come into contact.
Chi-Square test in pytest is used to compare the actual data for random positions of the box as well as the breaking distance of the car
to measure accuracy.

### Running the Code
Make sure you have python3 installed along with the necessary libraries (ex. pygame, pytest, etc.) <br>
On terminal run python3 main.py <br>
To run pytest run the command python3 -m pytest -s --cov


### Contributors 
Tharuni Iranjan - [TharuniI](https://github.com/TharuniI) <br>


https://user-images.githubusercontent.com/90390504/231201068-5c32027e-eb95-432f-8b1f-19f2d1a37170.mp4
