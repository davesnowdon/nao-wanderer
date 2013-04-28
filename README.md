nao-wanderer
============

Application for the NAO humanoid robot that makes it explore a space and
construct a map of its environment. Currently it's in a very basic state.

Code notes
----------
util.naoutil.NaoEnvironment is used to hold details of the NAO environment such as the calling choreographe box (if any), ALProxy objects and abstract the logging implementation. Most functions take an instance of NaoEnvironment as their first parameter.

Subclasses of wanderer.wanderer.Planner generate plans (lists of actions) in response to events raised by other components. Currently the only concrete Planner implementation is wanderer.randomwalk.RandomWalk.

wanderer.wanderer.PlanExecutor (or subclasses) are responsible for executing the next action in the plan. PlanExecutor provides hooks such as have_moved() to allow subclasses to trigger specific processing when the appropriate conditions are reached.


ALMemory
--------
ALMemory can not store custom classes, so when storing events and actions they are first converted to JSON strings using util.general.to_json_string() and reconstituted using from_json_string() - these functions rely on the classes implementing the to_json instance method and the from_json class method to make JSON serialisation possible.


The following ALMemory locations are used.

Configuration
* WandererSecurityDistance - closest distance in metres that we approach to an obstacle
* WandererLookForFaces - true if robot should be looking for faces while walking

Storing state
* WandererWalkPath - list of 6DOF robot positions representating the path the robot has followed so far
* WandererWalkHeading - direction (rotation about vertical axis) robot is walking in
* WandererFaceDirection - direction to detected face
* WandererEvent - event raised (stored as JSON)
* WandererActionsPlanned - list of planned actions (stored as JSON)
* WandererActionsInProgress - action currently being executed, NullAction if nothing to do (stored as JSON)
* WandererActionsCompleted - actions that have completed exeuction  (stored as JSON)

Web Interface
-------------
There is a web UI which is served from [ROBOT IP]:8080/index.html and the robot will also respond with JSON data to other requests such as:

* /actions/done - return list of completed actions
* /actions/planned - return list of planned acctions
* /actions/current - return actions in progress
* /raw/path - return the path the robot has followed
* /map/json - return a representation of the current map of the environment that NAO is exploring
