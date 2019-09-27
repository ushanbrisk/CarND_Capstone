# Udacity Capstone Project Team Doudoufei
> This is the project repo for the final project of the Udacity Self-Driving Car Nanodegree: Programming a Real Self-Driving Car. For more information about the project, see the project introduction [here](https://classroom.udacity.com/nanodegrees/nd013/parts/6047fe34-d93c-4f50-8336-b70ef10cb4b2/modules/e1a23b06-329a-4684-a717-ad476f0d8dff/lessons/462c933d-9f24-42d3-8bdc-a08a5fc866e4/concepts/5ab4b122-83e6-436d-850f-9f4d26627fd9).

Team member:
* Yongzhi Liu
* Yan Zhang
* Yanyan PENG
* Rajiv Sreedhar
* Pradhap Moorthi

- [Overall Structure](#heading)
  * [Perception](#sub-heading)
    + [Traffic Light Detection](#sub-sub-heading)
    + [Traffic Light Classification](#sub-sub-heading)
  * [Planning](#sub-heading)
    + [Waypoint Loader](#sub-sub-heading)
    + [Waypoint Updater](#sub-sub-heading)
  * [Control](#sub-heading)
    + [DBW](#sub-sub-heading)
    + [Waypoint Follower](#sub-sub-heading)

- [Environment](#heading-1)
<!-- toc -->

## Overall Structure
In this project, we used ROS nodes to implement the core functionality of the autonomous vehicle system, including traffic light detection, control, and waypoint following. The following is a system architecture diagram showing the [ROS](http://wiki.ros.org/) nodes and topics used in the project. 

![System architecture Diagram](imgs/final-project-ros-graph-v2.png)

### Perception
In this project, the perception is mainly from camera images for traffic light detection. The self driving car for this project is mainly for highway or test site without any obstacle. So no obstacle detection is considered.

#### Traffic Light Detection (tl_detector.py + tl_classfier.py)
* Input: 
  * /image_color: 
  * /current_pose: the vehicle's current position,
  * /base_waypoints: a complete list of reference waypoints the car will be following,
* Output: 
  * /traffic_waypoint: the locations to stop for red traffic lights

The traffic light detection node is within the tl_detector.py, and the traffic light classification node is within /tl_detector/light_classification_model/tl_classfier.py.

#### Traffic Light Classification

### Planning 

The path planning for this project is simply to produce a trajectory that obeys the traffic light.

#### Waypoint Loader
A package which loads the static waypoint data and publishes to /base_waypoints.

#### Waypoint Updater (waypoint_updater.py)
The purpose of this node is to update the target velocity property of each waypoint based on traffic light data. 
* Input: 
  * /base_waypoints, 
  * /current_pose, 
  * /traffic_waypoint
* Output: 
  * /final_waypoints: a list of waypoints ahead of the car with target velocities.

### Control (twist_controller.py)
Carla is equipped with a drive-by-wire (dbw) system, meaning the throttle, brake, and steering have electronic control. This package contains the files that are responsible for control of the vehicle: the node dbw_node.py and the file twist_controller.py, along with a pid and lowpass filter.

#### DBW
* Input:
  * /current_velocity
  * /twist_cmd: target linear and angular velocities. 
  * /vehicle/dbw_enabled: indicates if the car is under dbw or manual driver control. 
* Output:
  * /vehicle/throttle_cmd
  * /vehicle/brake_cmd
  * /vehicle/steering_cmd

#### Waypoint Follower
A package containing code from Autoware which subscribes to /final_waypoints and publishes target vehicle linear and angular velocities in the form of twist commands to the /twist_cmd topic. 

## Environment

Please use **one** of the two installation options, either native **or** docker installation.

### Native Installation

* Be sure that your workstation is running Ubuntu 16.04 Xenial Xerus or Ubuntu 14.04 Trusty Tahir. [Ubuntu downloads can be found here](https://www.ubuntu.com/download/desktop).
* If using a Virtual Machine to install Ubuntu, use the following configuration as minimum:
  * 2 CPU
  * 2 GB system memory
  * 25 GB of free hard drive space

  The Udacity provided virtual machine has ROS and Dataspeed DBW already installed, so you can skip the next two steps if you are using this.

* Follow these instructions to install ROS
  * [ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu) if you have Ubuntu 16.04.
  * [ROS Indigo](http://wiki.ros.org/indigo/Installation/Ubuntu) if you have Ubuntu 14.04.
* [Dataspeed DBW](https://bitbucket.org/DataspeedInc/dbw_mkz_ros)
  * Use this option to install the SDK on a workstation that already has ROS installed: [One Line SDK Install (binary)](https://bitbucket.org/DataspeedInc/dbw_mkz_ros/src/81e63fcc335d7b64139d7482017d6a97b405e250/ROS_SETUP.md?fileviewer=file-view-default)
* Download the [Udacity Simulator](https://github.com/udacity/CarND-Capstone/releases).

### Docker Installation
[Install Docker](https://docs.docker.com/engine/installation/)

Build the docker container
```bash
docker build . -t capstone
```

Run the docker file
```bash
docker run -p 4567:4567 -v $PWD:/capstone -v /tmp/log:/root/.ros/ --rm -it capstone
```

### Port Forwarding
To set up port forwarding, please refer to the "uWebSocketIO Starter Guide" found in the classroom (see Extended Kalman Filter Project lesson) or [instructions from term 2](https://classroom.udacity.com/nanodegrees/nd013/parts/40f38239-66b6-46ec-ae68-03afd8a601c8/modules/0949fca6-b379-42af-a919-ee50aa304e6a/lessons/f758c44c-5e40-4e01-93b5-1a82aa4e044f/concepts/16cf4a78-4fc7-49e1-8621-3450ca938b77).

### Usage

1. Clone the project repository
```bash
git clone https://github.com/udacity/CarND-Capstone.git
```

2. Install python dependencies
```bash
cd CarND-Capstone
pip install -r requirements.txt
```
3. Make and run styx
```bash
cd ros
catkin_make
source devel/setup.sh
roslaunch launch/styx.launch
```
4. Run the simulator

### Real world testing
1. Download [training bag](https://s3-us-west-1.amazonaws.com/udacity-selfdrivingcar/traffic_light_bag_file.zip) that was recorded on the Udacity self-driving car.
2. Unzip the file
```bash
unzip traffic_light_bag_file.zip
```
3. Play the bag file
```bash
rosbag play -l traffic_light_bag_file/traffic_light_training.bag
```
4. Launch your project in site mode
```bash
cd CarND-Capstone/ros
roslaunch launch/site.launch
```
5. Confirm that traffic light detection works on real life images

### Other library/driver information
Outside of `requirements.txt`, here is information on other driver/library versions used in the simulator and Carla:

Specific to these libraries, the simulator grader and Carla use the following:

|        | Simulator | Carla  |
| :-----------: |:-------------:| :-----:|
| Nvidia driver | 384.130 | 384.130 |
| CUDA | 8.0.61 | 8.0.61 |
| cuDNN | 6.0.21 | 6.0.21 |
| TensorRT | N/A | N/A |
| OpenCV | 3.2.0-dev | 2.4.8 |
| OpenMP | N/A | N/A |

