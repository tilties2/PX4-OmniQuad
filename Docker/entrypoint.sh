#!/bin/bash

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

repo_folder="/root/PX4-OmniQuad"
ws_folder="/root/ros2_ws"

cd $repo_folder

git config --global --add safe.directory "*"

echo -e "${YELLOW}STARTING SETUP OF THE REPO${NC}"
echo -e "--------------------------"

source /opt/ros/foxy/setup.bash

if [ ! -d "$repo_folder/build" ]; then
    # Build PX4 without simulation
    echo -e "${GREEN}BUILDING PX4 SITL ...${NC}"
    echo -e "--------------------------"
    sleep 5

    no_sim=1 make px4_sitl

    echo -e "wait little bit more ..."
    sleep 5

    # Build PX4 with Gazebo classic NDT tilting simulation
    echo -e "${GREEN}BUILDING PX4 SITL TILTES...${NC}"
    echo -e "--------------------------"
    DONT_RUN=1 make px4_sitl
fi

# Build ros2 packages
cd $ws_folder
if [ ! -d "$repo_folder/build" ]; then
    echo -e "${GREEN}BUILDING ros2 workspace ...${NC}"
    echo -e "--------------------------"
    colcon build
fi


echo -e "${GREEN}Setup completed, you can start using the container!${NC}"
exec "$@"
