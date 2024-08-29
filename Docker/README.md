# Deal with Omniquad Software in the loop

## Preliminaries steps

Setup the repos and the workspace: `./setup.sh`


## Docker compose (recommended)

1. Create docker image:
`docker compose build omniquad-sitl`

2. Create a container from the image: `docker compose up omniquad-sitl`
3. Open a new terminal inside the container:`docker exec-it omniquad-sitl-cnt zsh`

## Use bash files

Create docker image: `./create_image.sh`\
Launch docker container (ndivia): `./launch_docker.sh` \
Launch docker container (no nvidia): `./launch_no_nvidia.sh`

## Known issue

### 'Error response from daemon: container ... is not running'

docker container start omniquad-sitl-cnt

### Docker permission denied

[fix-docker-got-permission-denied](https://stackoverflow.com/questions/48957195/how-to-fix-docker-got-permission-denied-issue)

## Developer roadmap

Roadmap for the developer of the repo:

- [x] integrate `entrypoint.sh` to automatic build PX4 SITL
- [ ] integrate *tmux* to automatic handle the terminal
