# PX4 Omniquad

[![Releases](https://img.shields.io/github/release/PX4/PX4-Autopilot.svg)](https://github.com/PX4/PX4-Autopilot/releases) [![DOI](https://zenodo.org/badge/22634/PX4/PX4-Autopilot.svg)](https://zenodo.org/badge/latestdoi/22634/PX4/PX4-Autopilot)

[![Nuttx Targets](https://github.com/PX4/PX4-Autopilot/workflows/Nuttx%20Targets/badge.svg)](https://github.com/PX4/PX4-Autopilot/actions?query=workflow%3A%22Nuttx+Targets%22?branch=master) [![SITL Tests](https://github.com/PX4/PX4-Autopilot/workflows/SITL%20Tests/badge.svg?branch=master)](https://github.com/PX4/PX4-Autopilot/actions?query=workflow%3A%22SITL+Tests%22)


This repository holds the modified [PX4](http://px4.io) flight control solution for *Omniquad* drone
presented in "Design and Control of an Omnidirectional Aerial Robot with a Miniaturized Haptic Joystick for Physical Interaction"

Fully actuated aerial robot proved their superiority for Aerial Physical Interaction (APhI) over the past years. This work proposes a minimal setup for aerial telemanipulation, enhancing accessibility of these technologies. The design and the control of a 6-Degrees of Freedom (DoF) joystick with 4-DoF haptic feedback is detailed. It is the first haptic device with standard Remote Controller (RC) form factor for APhI. By miniaturizing haptic device, it enhances RC with the sense of touch, increasing physical awareness. The goal is to give operators an extra sense, other than vision and sound, to help to perform safe APhI. To the best of the authors knowledge, this is the first teleoperation system able to decouple each single axis input command. On the omnidirectional quadrotor, by reducing the number of components with a new design,
we aim a simplified maintenance, and improved force and thrust to weight ratio. Open-sourced physic based simulation and successful preliminary flight tests highlighted the tool as promising for future APhI applications.

More info on the mechanical design of the platform can be found here [Haptic-Omniquad](https://github.com/tilties2/Haptic-OmniQuad.git)

CONTACT FLIGHT           |  FREE FLIGHT
:-------------------------:|:-------------------------:
![alt text](Media/omniquad_contactflight.GIF)  |  ![alt text](Media/omniquad_freeflight.GIF)


## How to cite

```bibtex
@misc{mellet2024designcontrolomnidirectionalaerial,
      title={Design and Control of an Omnidirectional Aerial Robot with a Miniaturized Haptic Joystick for Physical Interaction},
      author={Julien Mellet and Andrea Berra and Salvatore Marcellini and Miguel Angel Trujillo Soto and Guillermo Heredia and Fabio Ruggiero and Vincenzo Lippiello},
      year={2024},
      eprint={2410.09003},
      archivePrefix={arXiv},
      primaryClass={cs.RO},
      url={https://arxiv.org/abs/2410.09003},
}
```

## Setup

### Launch sitl with docker (recommended option)

To instead launch sitl using docker

1. [Install docker](https://docs.docker.com/engine/install/ubuntu/), [nvidia-docker](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) and [docker compose](https://docs.docker.com/compose/)

2. Update

```bash
sudo apt-get update
```

3. Clone the repository

```bash
git clone https://github.com/tilties2/PX4-OmniQuad.git
```

4. Go inside docker folder

```bash
cd PX4-OmniQuad/Docker
```

5. Build docker image

```bash
docker compose build omniquad-sitl
```

6. Create docker container and launch it

```bash
docker compose up -d omniquad-sitl
```

7. Create a terminal inside docker container

```bash
docker exec -it omniquad-sitl-cnt zsh
```

8. Build and launch sitl

```bash
make px4_sitl gazebo-classic_omniquad
```

### Launch sitl (without docker)

Further information regards PX4 Software-In-The-Loop can be found at the official website [Simulation](https://docs.px4.io/v1.14/en/simulation/)

1. Clone the repository

```bash
git clone https://github.com/tilties2/PX4-OmniQuad.git
```

2. Initialize submodules

```bash
cd PX4-Omniquad
git submodule update --init --recursive
```

3. Install dependencies

```bash
cd PX4-OmniQuad/Tools/setup
./ubuntu.sh
```

4. Build and launch sitl

```bash
cd PX4-OmniQuad
make px4_sitl gazebo-classic_omniquad
```

### Connect with ROS2 with docker

Further information on ROS2 with PX4 can be found here [ROS 2 User Guide ](http://docs.px4.io/main/en/ros2/user_guide)

1. Open new terminal inside the container

```bash
docker exec -it omniquad-sitl-cnt zsh
```

2. Start the agent and connect with ROS2

```bash
MicroXRCEAgent udp4 -p 8888
```
