nao-wanderer
============

Application for the NAO humanoid robot that makes it explore a space and
construct a map of its environment. Currently it's in a very basic state.

ALMemory
--------
The following ALMemory locations are used.

Configuration
* WandererSecurityDistance - closest distance in metres that we approach to an obstacle
* WandererLookForFaces - true if robot should be looking for faces while walking

Storing state
* WandererObstacleLocation - rough location of obstacle left, right, centre
* WandererWalkPath - list of 6DOF robot positions representating the path the robot has followed so far
* WandererWalkHeading - direction (rotation about vertical axis) robot is walking in
* WandererFaceDirection - direction to detected face

