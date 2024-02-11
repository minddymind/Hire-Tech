#!/bin/sh

# remove container
docker compose down

# clear cache and delete entire not used in docker
#yes is to auto interact "y" when prompt ask
yes | docker system prune -a

# fire up our docker container
./run_docker_compose.sh