# Partition Into Groups

[![Build Status](https://travis-ci.org/mariiuus/PIG.svg?branch=master)](https://travis-ci.org/mariiuus/PIG)
[![Coverage Status](https://coveralls.io/repos/github/mariiuus/PIG/badge.svg?branch=master)](https://coveralls.io/github/mariiuus/PIG?branch=master)

Read `CONTRIBUTING.md` for information about the project structure to get started contributing.

TDT4140 - Software Engineering

PIG, Partition Into Groups, is an application with the objective to intelligently partition a set of people into groups based on parameters that the users answer before being divided into groups.

Our application will provide functionality to create instances of divisions where different users can sign up as members to be placed in a group or leader to be leading a group. 

As a scenario you can imagine a lecturer creating a division for one of his courses so that the students taking the course can be divided into groups to do a group project. Also, teaching assistants can sign up as leaders for this division to be assigned a number of groups they are. 

Creators will be able to instantiate the partitioning of the members. They will also be able to se all the groups related to a specific division they have created. 

Leaders will be albe to se all the groups they have been assigned, and the members of the groups so that they can easily make contact through email.

For the process of partitioning the set of members signed up for a division we are looking at multiple different approaches. We either will be going for a clustering algorithm to solve the problem or we will look into a DP solution.
