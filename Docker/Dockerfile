FROM ubuntu:20.04 AS base

ENV DEBIAN_FRONTEND=noninteractive

# Install language
RUN apt-get update && apt-get install -y \
  locales \
  && locale-gen en_US.UTF-8 \
  && update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 \
  && rm -rf /var/lib/apt/lists/*
ENV LANG en_US.UTF-8

# solme basic packages
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    -y wget apt-utils git openssh-server nano \
    python3                  \
    python3-wstool             \
    python3-pip                \
    python-is-python3          \
    && rm -rf /var/lib/apt/lists/*

# Install timezone
RUN ln -fs /usr/share/zoneinfo/UTC /etc/localtime \
  && export DEBIAN_FRONTEND=noninteractive \
  && apt-get update \
  && apt-get install -y tzdata \
  && dpkg-reconfigure --frontend noninteractive tzdata \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get -y upgrade \
    && rm -rf /var/lib/apt/lists/*

# Install common programs
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    lsb-release \
    sudo \
    software-properties-common \
    wget \
    && rm -rf /var/lib/apt/lists/*

# zsh
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.2/zsh-in-docker.sh)" -- \
    -t agnoster \
    -p git \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-syntax-highlighting

# color bash
RUN sed -i 's/#force_color_prompt=yes/force_color_prompt=yes/g' ~/.bashrc

# fzf
WORKDIR /root/third_parties
RUN git clone https://github.com/junegunn/fzf.git
WORKDIR /root/third_parties/fzf
RUN /bin/zsh -c "./install"
WORKDIR /root

# cmake 3.20
WORKDIR /root/third_parties
RUN apt remove --purge --auto-remove cmake && \
    apt update && \
    apt install -y wget software-properties-common lsb-release && \
    wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | tee /etc/apt/trusted.gpg.d/kitware.gpg >/dev/null && \
    apt-add-repository "deb https://apt.kitware.com/ubuntu/ $(lsb_release -cs) main" && \
    apt update && \
    apt install -y kitware-archive-keyring && \
    rm /etc/apt/trusted.gpg.d/kitware.gpg && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 6AF7F09730B3F0A4 && \
    apt update && \
    apt install -y cmake && \
    apt clean all

# key issues
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 1A127079A92F09ED

# Install ROS2
RUN sudo add-apt-repository universe \
  && curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg \
  && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null \
  && apt-get update && apt-get install -y --no-install-recommends \
    ros-foxy-ros-base \
    python3-argcomplete \
  && rm -rf /var/lib/apt/lists/*

ENV ROS_DISTRO=foxy
ENV AMENT_PREFIX_PATH=/opt/ros/foxy
ENV COLCON_PREFIX_PATH=/opt/ros/foxy
ENV LD_LIBRARY_PATH=/opt/ros/foxy/lib
ENV PATH=/opt/ros/foxy/bin:$PATH
ENV PYTHONPATH=/opt/ros/foxy/lib/python3.10/site-packages
ENV ROS_PYTHON_VERSION=3
ENV ROS_VERSION=2
ENV DEBIAN_FRONTEND=

###########################################
#  Develop image
###########################################
FROM base AS dev

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y --no-install-recommends \
    build-essential \
    gdb \
    git \
    openssh-client \
    python3-argcomplete \
    python3-pip \
    ros-foxy-ament-* \
    && rm -rf /var/lib/apt/lists/*

RUN rosdep init || echo "rosdep already initialized"

# ARG USERNAME=ros
# ARG USER_UID=1000
# ARG USER_GID=$USER_UID

# Create a non-root user
# RUN groupadd --gid $USER_GID $USERNAME \
#   && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
#   # Add sudo support for the non-root user
#   && apt-get update \
#   && apt-get install -y sudo \
#   && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
#   && chmod 0440 /etc/sudoers.d/$USERNAME \
#   && rm -rf /var/lib/apt/lists/*

# Set up autocompletion for user
RUN apt-get update && apt-get install -y git-core bash-completion \
  && echo "if [ -f /opt/ros/${ROS_DISTRO}/setup.bash ]; then source /opt/ros/${ROS_DISTRO}/setup.bash; fi" >> /home/$USERNAME/.bashrc \
  && echo "if [ -f /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash ]; then source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash; fi" >> /home/$USERNAME/.bashrc \
  && rm -rf /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND=
ENV AMENT_CPPCHECK_ALLOW_SLOW_VERSIONS=1

###########################################
#  Full image
###########################################
FROM dev AS full

ENV DEBIAN_FRONTEND=noninteractive
# Install the full release
RUN apt-get update && apt-get install -y --no-install-recommends \
  ros-foxy-desktop \
  && rm -rf /var/lib/apt/lists/*
ENV DEBIAN_FRONTEND=

###########################################
#  Full+Gazebo image
###########################################
FROM full AS gazebo

ENV DEBIAN_FRONTEND=noninteractive
# Install gazebo
RUN wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg \
  && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null \
  && apt-get update && apt-get install -q -y --no-install-recommends \
    ros-$ROS_DISTRO-gazebo* \
  && rm -rf /var/lib/apt/lists/*
ENV DEBIAN_FRONTEND=

###########################################
#  Full+Gazebo+Nvidia image
###########################################

FROM gazebo AS gazebo-nvidia

################
# Expose the nvidia driver to allow opengl
# Dependencies for glvnd and X11.
################
RUN apt-get update \
 && apt-get install -y -qq --no-install-recommends \
  libglvnd0 \
  libgl1 \
  libglx0 \
  libegl1 \
  libxext6 \
  libx11-6

# Env vars for the nvidia-container-runtime.
ENV NVIDIA_VISIBLE_DEVICES ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}all
ENV QT_X11_NO_MITSHM 1


###########################################
#  PX4 image
###########################################

FROM gazebo-nvidia as px4
RUN pip3 install -U empy==3.3.4 pyros-genmsg setuptools
RUN apt install -y python3-colcon-common-extensions

# Clone and build Micro-XRCE-DDS-Agent
RUN git clone https://github.com/eProsima/Micro-XRCE-DDS-Agent.git /root/Micro-XRCE-DDS-Agent && \
    cd /root/Micro-XRCE-DDS-Agent && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    make install && \
    ldconfig /usr/local/lib/

# Clone PX4 repositories
RUN mkdir -p /root/ros2_ws/src/
WORKDIR /root/ros2_ws/srcº
RUN git clone https://github.com/PX4/px4_msgs.git
RUN git clone https://github.com/PX4/px4_ros_com.git
RUN git clone https://github.com/tilties2/ws_sensor_combined.git

# Build ws
WORKDIR /root/ros2_ws
RUN echo "source /opt/ros/$ROS_DISTRO/setup.zsh" >> ~/.zshrc
RUN /bin/zsh -c "source /opt/ros/$ROS_DISTRO/setup.zsh && colcon build"
RUN echo "source /root/ros2_ws/install/setup.zsh" >> ~/.zshrc

# from ubuntu.sh
WORKDIR /root/third_parties
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
RUN DEBIAN_FRONTEND=noninteractive apt-get -y --quiet --no-install-recommends install \
	astyle \
	build-essential \
	cmake \
	cppcheck \
	file \
	g++ \
	gcc \
	gdb \
	git \
	lcov \
	libfuse2 \
	libxml2-dev \
	libxml2-utils \
	make \
	ninja-build \
	python3 \
	python3-dev \
	python3-pip \
	python3-setuptools \
	python3-wheel \
	rsync \
	shellcheck \
	unzip \
	zip \
	automake \
	binutils-dev \
	bison \
	build-essential \
	flex \
	g++-multilib \
	gcc-multilib \
	gdb-multiarch \
	genromfs \
	gettext \
	gperf \
	libelf-dev \
	libexpat-dev \
	libgmp-dev \
	libisl-dev \
	libmpc-dev \
	libmpfr-dev \
	libncurses5 \
	libncurses5-dev \
	libncursesw5-dev \
	libtool \
	pkg-config \
	screen \
	texinfo \
	u-boot-tools \
	util-linux \
	vim-common \
  kconfig-frontends \
  libgstreamer-plugins-base1.0-dev

#entrypoint
WORKDIR /
COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/entrypoint.sh" ]
SHELL ["/bin/zsh", "-c"]
CMD ["zsh"]
