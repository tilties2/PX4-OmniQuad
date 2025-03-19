#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# check if NVIDIA Container Toolkit is installed
is_toolkit_installed() {
    dpkg -l | grep -q nvidia-container-toolkit
}

if is_toolkit_installed; then
    echo "NVIDIA Container Toolkit is already installed. Skipping installation."
else
    # Configure the repository
    echo "Configuring NVIDIA Container Toolkit repository..."
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

    curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
        sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
        sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

    # Update package lists
    echo "Updating package lists..."
    sudo apt-get update

    # Install NVIDIA Container Toolkit
    echo "Installing NVIDIA Container Toolkit..."
    sudo apt-get install -y nvidia-container-toolkit

    # Restart Docker service
    echo "Restarting Docker service..."
    sudo systemctl restart docker

    # Configure the container runtime
    echo "Configuring NVIDIA Container Toolkit runtime..."
    sudo nvidia-ctk runtime configure --runtime=docker

    # Restart Docker again
    echo "Restarting Docker service again..."
    sudo systemctl restart docker
fi

# Verify installation
echo "Verifying NVIDIA Container Toolkit installation..."
docker run --rm --runtime=nvidia --gpus all ubuntu nvidia-smi
