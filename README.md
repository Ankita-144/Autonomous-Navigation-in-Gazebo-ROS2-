# Autonomous Navigation in Gazebo (ROS2)

This project is an attempt to implement map-less autonomous navigation using ROS2, Gazebo, and sensor fusion. The system combines LiDAR-based obstacle avoidance with ArUco marker detection to guide decision-making in a simulated environment.

## Problem Context

This project is based on the UGV Autonomous Navigation Challenge, which requires:

* Map-less navigation (no SLAM or AMCL)
* Detection of ArUco markers and directional signs
* Navigation through a multi-zone arena including maze and intersections
* Completion of the mission using only local perception and reactive planning 

## What I Implemented

* Custom Gazebo simulation environment (arena with markers)
* ROS2 node for decision-making
* ArUco marker detection pipeline
* LiDAR-based obstacle detection
* Sensor fusion logic combining vision and LiDAR inputs
* Velocity control using `/cmd_vel`

## System Architecture

The main control logic is implemented in a ROS2 node:

* Subscribes to:

  * ArUco marker topic (`/aruco_id`)
  * LiDAR scan (`/r1_mini/lidar`)
* Publishes:

  * Velocity commands (`/cmd_vel`)

### Decision Logic

* ArUco detection is given priority (temporary override)
* If no marker is detected → fallback to LiDAR navigation
* Reactive obstacle avoidance is used instead of global planning

## Current Status

The system is partially functional:

* ArUco detection works and triggers control actions
* Basic navigation logic is implemented
* However, wall detection and stable navigation are not fully reliable

## Challenges Faced

* LiDAR-based wall detection inconsistencies
* Difficulty tuning navigation parameters in map-less setup
* Balancing perception inputs (ArUco vs LiDAR)
* Lack of global context without SLAM

## What I Learned

* ROS2 node architecture and communication
* Sensor fusion between vision and LiDAR
* Reactive navigation strategies
* Debugging simulation-based robotics systems

## Tech Stack

* ROS2 (rclpy)
* Gazebo
* Python
* LiDAR + Camera sensors

## Future Improvements

* Improve LiDAR processing for reliable wall detection
* Implement better obstacle avoidance strategies
* Add recovery behaviors (rotate, backtrack)
* Improve navigation stability in maze environments

## Note

This is a work-in-progress project focused on learning autonomous navigation in simulation. The goal was to explore perception-driven navigation without relying on pre-built maps.

## Authors 
Ankita Kumari
