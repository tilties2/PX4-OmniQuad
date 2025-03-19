import os
import subprocess
import sys


class DockerManager:
    def __init__(
        self,
        docker_compose_file="docker-compose.yml",
        container_name="omniquad-sitl-cnt",
    ):
        self.docker_compose_file = docker_compose_file
        self.container_name = container_name

    def is_docker_installed(self):
        """Check if Docker is installed."""
        try:
            subprocess.run(
                ["docker", "--version"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            return True
        except FileNotFoundError:
            return False

    def has_nvidia_driver(self):
        """Check if the system has an NVIDIA driver installed."""
        try:
            subprocess.run(
                ["nvidia-smi"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            return True
        except FileNotFoundError:
            return False

    def has_nvidia_toolkit_installed(self):
        """Check if the system has NVIDIA driver toolkit installed"""
        try:
            result = subprocess.run(
                "dpkg -l | grep -i nvidia-container",
                check=True,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # check if output is non-empty
            if result.stdout:
                return True
            else:
                return False

        except subprocess.CalledProcessError:
            return False

    def install_docker(self):
        """Installs Docker using the official installation script if not already installed."""
        if self.is_docker_installed():
            print("Docker is already installed.")
        else:
            print("Installing Docker...")
            os.system(
                "curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh"
            )

        if self.has_nvidia_driver():
            if not self.has_nvidia_toolkit_installed():
                print("Installing NVIDIA Docker...")
                os.system(
                    "chmod +x install_nvidia_docker.sh && sudo ./install_nvidia_docker.sh"
                )
                print("Docker and NVIDIA Docker installation complete.")
            else:
                print("NVIDIA Driver Toolkit already installed.")
        else:
            print("No NVIDIA driver detected. Skipping NVIDIA Docker installation.")

    def start_docker(self):
        """Builds and starts the Docker container using docker-compose."""
        print("Starting Docker container...")
        os.system(f"docker compose -f {self.docker_compose_file} up -d --build")
        print("Docker container started.")

    def open_terminal(self):
        """Opens a new terminal session inside the running Docker container."""
        print(f"Opening a terminal in container {self.container_name}...")
        os.system(f"docker exec -it {self.container_name} /bin/zsh")

    def close_container(self):
        """Close docker container"""
        print("Closing the Docker container ...")
        os.system(f"docker stop {self.container_name}")

    def print_help(self):
        """Prints usage instructions."""
        print(
            """
Usage: python docker_manager.py [install|start|open|--help]]

Commands:
  install   Install Docker and NVIDIA Docker.
  start     Build and start the Docker container using docker-compose.
  open      Open a new terminal session inside a running Docker container.
  stop      Stop Docker container.
  --help    Show this help message.
        """
        )


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "--help":
        DockerManager().print_help()
        sys.exit(0)

    mode = sys.argv[1]
    manager = DockerManager()

    if mode == "install":
        manager.install_docker()
    elif mode == "start":
        manager.start_docker()
    elif mode == "open":
        manager.open_terminal()
    elif mode == "stop":
        manager.close_container()
    else:
        print("Invalid mode. Use '--help' for usage instructions.")
        sys.exit(1)
