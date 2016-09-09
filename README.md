# "Programming Robots with ROS sample code"

This repository contains all the examples from the book "Programming Robots
with ROS", by Morgan Quigly, Brian Gerkey and William D. Smart (O'Reilly Media,
Inc., 2015).

The code is originally written and copyright by Morgan Quigly, Brian Gerkey and
William D. Smart.

The examples have had bug fixes applied, where those bugs have been found.

The code is organised by chapters, with one package per chapter. For most
chapters, the examples give file names. The code in this repository uses these
file names to make the examples easy to relate to the book and easy to use from
each other (e.g. when launching nodes from launch files). For examples where
file names are not provided (primarily the examples in chapters 16, 17 and 18,
where a single file is gradually built up throughout the chapter), the files in
this repository are instead named after the example numbers.

The examples have been tested on Indigo. All examples except for chapters 11
and 14 (due to lack of required support packages) have also been tested on
Kinetic; chapter 12 currently is buggy in Kinetic - the line does not show up
in Gazebo.
